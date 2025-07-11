# GhostVault 👻🔒

A cross-platform Python tool for text-based steganography on image and audio files. Hide secret messages in plain sight!

**Created by ACT91**  
**GitHub:** [https://github.com/ACT91](https://github.com/ACT91)

## Features

- **Image Steganography**: Hide messages in PNG, JPG, JPEG files using LSB (Least Significant Bit) technique
- **Audio Steganography**: Hide messages in WAV files using LSB technique
- **Password Protection**: Optional AES encryption for enhanced security
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **CLI Interface**: Simple command-line interface for easy usage

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. **Optional - For MP3 conversion**: Install FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add to your system PATH

## Usage

### Interactive Mode (Recommended)

Run the interactive interface:
```bash
python ghostvault.py
# or
python3 ghostvault.py
```

The tool will display a colorful logo and menu:
- **Option 1 - Hide Me**: Hide messages in images or audio files
- **Option 2 - Reveal Me**: Scan and extract hidden messages
- **Option 3 - Exit**: Close the application

### CLI Mode (Advanced)

Run the command-line interface:
```bash
python ghostvault_cli.py
```

**Hide a message:**
```bash
python ghostvault_cli.py hide --file input.png --message "Secret message" --output output.png
```

**Extract a message:**
```bash
python ghostvault_cli.py extract --file output.png
```

## Supported Formats

- **Images**: PNG, JPG, JPEG
- **Audio**: WAV (primary), MP3 (converts to WAV automatically)

## How It Works

### LSB Steganography
- **Images**: Modifies the least significant bit of each pixel's color values
- **Audio**: Modifies the least significant bit of each audio sample
- Messages are terminated with a special delimiter (`###END###`)

### Encryption
- Uses AES encryption via the `cryptography` library
- Password-based key derivation with PBKDF2
- Salt is prepended to encrypted data for security

## Project Structure

```
ghostvault/
├── ghostvault.py        # Interactive interface (main)
├── ghostvault_cli.py    # CLI interface
├── steg/
│   ├── image_steg.py    # Image steganography functions
│   ├── audio_steg.py    # Audio steganography functions
│   └── crypto.py        # Encryption/decryption
├── utils/
│   └── validator.py     # File validation utilities
├── extracted_messages/  # Auto-created folder for extracted messages
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Features & Notes

- **Auto File Extension**: Output files automatically use the same extension as input
- **Organized Output**: Extracted messages saved in `extracted_messages/` folder as `.txt` files
- **MP3 Conversion**: Automatically converts MP3 to WAV (requires FFmpeg)
- **Dual Message Display**: Shows both encrypted and decrypted versions when revealing
- **Performance**: Processing time varies with file size - larger WAV files take longer

## Error Handling

- Validates file formats and paths
- Checks if message is too long for cover file
- Handles encryption/decryption errors
- Provides clear error messages
- Offers MP3 conversion options

## Security Notes

- LSB steganography is detectable by statistical analysis
- Use password protection for sensitive messages
- Encrypted messages are base64 encoded for storage
- Consider the security implications of your use case

## Performance Notes

- Processing time depends on file size
- Large WAV files (>10MB) may take several seconds to process
- MP3 conversion requires additional processing time

## Author

**ACT91**  
GitHub: [https://github.com/ACT91](https://github.com/ACT91)

## License

This tool is for educational and legitimate purposes only. Users are responsible for compliance with applicable laws and regulations.

Created with ❤️ by ACT91