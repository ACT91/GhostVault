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

**Hide a message:**
```bash
python main.py hide --file input.png --message "Secret message" --output output.png
```

**Extract a message:**
```bash
python main.py extract --file output.png
```

## Supported Formats

- **Images**: PNG, JPG, JPEG
- **Audio**: WAV

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
├── main.py              # CLI entry point
├── steg/
│   ├── image_steg.py    # Image steganography functions
│   ├── audio_steg.py    # Audio steganography functions
│   └── crypto.py        # Encryption/decryption
├── utils/
│   └── validator.py     # File validation utilities
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Error Handling

- Validates file formats and paths
- Checks if message is too long for cover file
- Handles encryption/decryption errors
- Provides clear error messages

## Security Notes

- LSB steganography is detectable by statistical analysis
- Use password protection for sensitive messages
- Consider the security implications of your use case

## Author

**ACT91**  
GitHub: [https://github.com/ACT91](https://github.com/ACT91)

## License

This tool is for educational and legitimate purposes only. Users are responsible for compliance with applicable laws and regulations.

Created with ❤️ by ACT91