# Py Video Converter

This script converts video files from various formats to a specified output format using FFmpeg. It detects the type of GPU available (NVIDIA or AMD) and uses the appropriate video encoder for conversion. If no GPU is found, it defaults to CPU encoding.

## Requirements

- Python 3.x
- FFmpeg installed and accessible via the system PATH

## Usage

### Command-line Arguments

- `-d`, `--directory`: Directory where the video files are located. (Required)
- `-i`, `--input_formats`: Input formats of the files to be converted (e.g., .mp4 .ts). If not provided, all video files will be converted. (Optional)
- `-o`, `--output_format`: Output format of the converted files (default: .mkv). (Optional)

### Example

To convert all `.mp4` and `.ts` files in the `videos` directory to `.mkv` format:

```sh
python video_converter.py -d /path/to/videos -i .mp4 .ts -o .mkv
```

To convert all video files in the `videos` directory to `.mkv` format:

```sh
python video_converter.py -d /path/to/videos -o .mkv
```

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install FFmpeg and ensure it is accessible via the system PATH.
3. Clone this repository.

## Functionality

1. **GPU Detection**:
    - Detects NVIDIA GPUs using `nvidia-smi`.
    - Detects AMD GPUs using `wmic` on Windows.
    - Defaults to CPU if no GPU is found.

2. **FFmpeg Version Check**:
    - Checks if FFmpeg is installed and retrieves its version.

3. **Video Conversion**:
    - Recursively scans the specified directory for video files.
    - Converts eligible files to the specified output format using the appropriate video encoder.
    - Moves original files to an `old` directory after conversion.

## Script Details

### `detect_gpu()`

Detects the type of GPU available (NVIDIA or AMD) or defaults to CPU.

### `verifica_ffmpeg()`

Checks if FFmpeg is installed and returns its version.

### Argument Parsing

Uses `argparse` to handle command-line arguments.

### Main Process

1. Checks FFmpeg version.
2. Lists video files in the specified directory.
3. Detects GPU type.
4. Chooses the appropriate video encoder.
5. Converts video files using FFmpeg.
6. Moves original files to an `old` directory.

## License

This project is licensed under the MIT License.
