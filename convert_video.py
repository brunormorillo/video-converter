import os
import subprocess
import argparse
import sys

def detect_gpu():
    try:
        # Tenta identificar GPUs NVIDIA
        nvidia_info = subprocess.check_output(['nvidia-smi', '-L']).decode('utf-8')
        if "GPU" in nvidia_info:
            return "nvidia"
    except Exception:
        pass

    try:
        # Tenta identificar GPUs AMD via comando Windows
        amd_info = subprocess.check_output(['wmic', 'path', 'win32_VideoController', 'get', 'name']).decode('utf-8')
        if "AMD" in amd_info or "Radeon" in amd_info:
            return "amd"
    except Exception:
        pass

    # Se não encontrar GPUs NVIDIA ou AMD, assume uso da CPU
    return "cpu"

def verifica_ffmpeg():
    try:
        # Tenta capturar a versão do FFmpeg
        ffmpeg_version_info = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode('utf-8')
        for line in ffmpeg_version_info.split('\n'):
            if 'ffmpeg version' in line:
                return line
    except FileNotFoundError:
        return "ffmpeg não localizado em c:/Program Files/ffmpeg/bin"
    return "ffmpeg não localizado"

# Configura o analisador de argumentos
parser = argparse.ArgumentParser(description="Converte arquivos de vídeo para um formato específico.")
parser.add_argument('-d', '--directory', type=str, required=True, help="Diretório onde os vídeos estão localizados.")
parser.add_argument('-i', '--input_formats', nargs='*', default=None, help="Formatos de entrada dos arquivos a serem convertidos (ex: .mp4 .ts). Se nenhum for fornecido, todos os arquivos de vídeo serão convertidos.")
parser.add_argument('-o', '--output_format', type=str, default='.mkv', help="Formato de saída dos arquivos convertidos (padrão: .mkv).")
args = parser.parse_args()

# Exibe a versão do FFmpeg
ffmpeg_version = verifica_ffmpeg()
print(ffmpeg_version)

# Define o diretório onde estão os arquivos de vídeo
diretorio = args.directory

# Lista todos os arquivos de vídeo em todos os subdiretórios
arquivos_para_converter = []
for root, dirs, files in os.walk(diretorio):
    for file in files:
        # Verifica se o arquivo não está no formato de saída
        if not file.endswith(args.output_format):
            # Verifica todos os arquivos se nenhum formato de entrada foi especificado
            if args.input_formats is None or any(file.endswith(ext) for ext in args.input_formats):
                arquivos_para_converter.append(os.path.join(root, file))

# Total de arquivos a serem convertidos
total_arquivos = len(arquivos_para_converter)
print(f"Iniciando a conversão de {total_arquivos} arquivos...")

gpu_type = detect_gpu()
print(f"Usando {gpu_type.upper()} para processamento.")

# Escolhe o encoder baseado no tipo de GPU ou CPU
if gpu_type == "nvidia":
    video_encoder = "hevc_nvenc"
elif gpu_type == "amd":
    video_encoder = "hevc_amf"
else:
    video_encoder = "libx265"  # Pode usar libx264 para H.264

# Se houver arquivos para converter, continua o processo
if total_arquivos > 0:
    # Cria o diretório "old" se ele não existir
    diretorio_old = os.path.join(diretorio, 'old')
    if not os.path.exists(diretorio_old):
        os.mkdir(diretorio_old)

    # Percorre todos os arquivos elegíveis e converte um a um
    for arquivo in arquivos_para_converter:
        nome_completo = arquivo
        nome_saida = os.path.splitext(nome_completo)[0] + args.output_format
        print(f"Arquivo iniciado o processamento: {os.path.basename(nome_completo)}")

        # Comando para converter o arquivo usando o encoder escolhido
        comando = ['ffmpeg', '-i', nome_completo, '-c:v', video_encoder, '-c:a', 'copy', nome_saida]
        process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Captura e exibe apenas a linha mais recente dos logs do FFmpeg
        for line in process.stdout:
            if 'frame=' in line:
                sys.stdout.write('\r' + line.strip())
                sys.stdout.flush()

        process.wait()  # Aguarda a conclusão do processo FFmpeg
        print(f"\nArquivo finalizado o processamento: {os.path.basename(nome_completo)}")

        # Prepara o diretório 'old' correspondente ao arquivo
        diretorio_old_local = os.path.join(os.path.dirname(nome_completo), 'old')
        if not os.path.exists(diretorio_old_local):
            os.mkdir(diretorio_old_local)

        # Move o arquivo original para a pasta "old"
        os.rename(nome_completo, os.path.join(diretorio_old_local, os.path.basename(arquivo)))

    print("Conversão concluída!")
else:
    print("Nenhum arquivo para converter encontrado.")
