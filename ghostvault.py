#!/usr/bin/env python3
import os
import sys
from steg.image_steg import hide_in_image, extract_from_image
from steg.audio_steg import hide_in_audio, extract_from_audio
from utils.validator import validate_file, check_capacity

def print_logo():
    """Display GhostVault logo with colors."""
    logo = """
\033[92m  ██████  ██   ██  ██████  ███████ ████████ \033[91m██    ██  █████  ██    ██ ██   ████████ 
\033[92m ██       ██   ██ ██    ██ ███        ██    \033[91m██    ██ ██   ██ ██    ██ ██      ██    
\033[92m ██   ███ ███████ ██    ██ ███████    ██    \033[91m██    ██ ███████ ██    ██ ██      ██    
\033[92m ██    ██ ██   ██ ██    ██      ██    ██    \033[91m ██  ██  ██   ██ ██    ██ ██      ██    
\033[92m  ██████  ██   ██  ██████  ███████    ██    \033[91m  ████   ██   ██  ██████  ███████ ██    
\033[0m
\033[96m                    Text-based Steganography Tool\033[0m
\033[93m                         Hide in Plain Sight\033[0m
\033[95m                      Created by ACT91\033[0m
\033[94m                   GitHub: https://github.com/ACT91\033[0m
\033[94m                   Don't Forget To Leave a Star on this Project : https://github.com/ACT91/GhostVault \033[0m
"""
    print(logo)

def scan_file(file_path):
    """Scan file to detect if it contains hidden data."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg']:
            message = extract_from_image(file_path)
        elif ext == '.wav':
            message = extract_from_audio(file_path)
        else:
            return None, None
        
        if message:
            # Try to detect if it's encrypted - check for base64 pattern
            try:
                import base64
                # Try to decode as base64 - if successful and contains binary data, likely encrypted
                decoded = base64.b64decode(message)
                is_encrypted = len(decoded) > 16 and len(message) > 20
            except:
                # Check for non-printable characters or base64-like patterns
                is_encrypted = any(ord(c) > 127 or (ord(c) < 32 and c not in '\n\r\t') for c in message[:50])
            
            return "text", is_encrypted
        return None, None
    except:
        return None, None

def convert_audio(file_path):
    """Convert MP3 to WAV format."""
    try:
        from pydub import AudioSegment
        
        # Load MP3 file
        audio = AudioSegment.from_mp3(file_path)
        
        # Create output path
        dir_path = os.path.dirname(file_path)
        filename = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(dir_path, f"converted_{filename}.wav")
        
        # Export as WAV
        audio.export(output_path, format="wav")
        
        return output_path
    except ImportError:
        print("\033[91mError: pydub library required for conversion. Install with: pip install pydub\033[0m")
        return None
    except FileNotFoundError:
        print("\033[91mError: FFmpeg not found. Please install FFmpeg or use online converter to convert MP3 to WAV\033[0m")
        print("\033[93mAlternative: Use an online MP3 to WAV converter and save the file manually\033[0m")
        return None
    except Exception as e:
        print(f"\033[91mConversion failed: {str(e)}\033[0m")
        print("\033[93mTip: Use an online converter or audio editing software to convert MP3 to WAV\033[0m")
        return None

def hide_menu():
    """Handle hide operations."""
    print("\n\033[92m=== HIDE MESSAGE ===\033[0m")
    print("1. Hide in Image")
    print("2. Hide in Audio")
    
    choice = input("\nSelect option (1-2): ").strip()
    
    if choice not in ['1', '2']:
        print("\033[91mInvalid choice!\033[0m")
        return
    
    file_path = input("Enter file path: ").strip().strip('"')
    
    if not validate_file(file_path):
        # Check if it's an MP3 file for audio option
        if choice == '2' and file_path.lower().endswith('.mp3'):
            print("\033[93mMP3 format detected. Choose an option:\033[0m")
            print("1. Convert to WAV")
            print("2. Use another file (.wav)")
            
            convert_choice = input("Select option (1-2): ").strip()
            
            if convert_choice == '1':
                print("\033[96mConverting MP3 to WAV...\033[0m")
                converted_path = convert_audio(file_path)
                if converted_path:
                    print(f"\033[92mConversion successful: {os.path.basename(converted_path)}\033[0m")
                    print("\033[96mGo back and use the converted file.\033[0m")
                else:
                    print("\033[93mConversion failed. Please convert manually or use a WAV file.\033[0m")
                return
            elif convert_choice == '2':
                print("\033[96mPlease select a WAV file.\033[0m")
                return
        
        print("\033[91mError: Invalid or unsupported file!\033[0m")
        return
    
    message = input("Enter secret message: ").strip()
    
    if not check_capacity(file_path, message):
        print("\033[91mError: Message too long for the cover file!\033[0m")
        return
    
    output_name = input("Enter output filename (without extension): ").strip()
    
    # Get the same extension as input file
    input_ext = os.path.splitext(file_path)[1]
    output_path = os.path.join(os.path.dirname(file_path), output_name + input_ext)
    
    use_password = input("Use password protection? (y/n) - y=YES & n=NO : ").strip().lower()
    password = None
    if use_password == 'y':
        password = input("Enter password: ").strip()
    
    try:
        if choice == '1':
            hide_in_image(file_path, message, output_path, password)
        else:
            hide_in_audio(file_path, message, output_path, password)
        
        print(f"\033[92mMessage successfully hidden in {output_path}\033[0m")
    except Exception as e:
        print(f"\033[91mError: {str(e)}\033[0m")

def reveal_menu():
    """Handle reveal operations."""
    print("\n\033[93m=== REVEAL MESSAGE ===\033[0m")
    
    # Create extracted_messages folder if it doesn't exist
    if not os.path.exists("extracted_messages"):
        os.makedirs("extracted_messages")
    
    file_path = input("Enter file path to scan: ").strip().strip('"')
    
    if not validate_file(file_path):
        print("\033[91mError: Invalid or unsupported file!\033[0m")
        return
    
    print("\n\033[96mScanning file...\033[0m")
    content_type, is_encrypted = scan_file(file_path)
    
    if not content_type:
        print("\033[91mNo hidden message found in this file.\033[0m")
        return
    
    print(f"\033[92mHidden content detected: {content_type.upper()}\033[0m")
    
    password = None
    if is_encrypted:
        print("\033[93mContent appears to be encrypted.\033[0m")
        password = input("Enter password (or press Enter to try without): ").strip()
        password = password if password else None
    
    print("\n1. Extract Message")
    choice = input("Select option (1): ").strip()
    
    if choice != '1':
        print("\033[91mInvalid choice!\033[0m")
        return
    
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # First extract raw message without decryption
        if ext in ['.png', '.jpg', '.jpeg']:
            raw_message = extract_from_image(file_path)
            if password:
                decrypted_message = extract_from_image(file_path, password)
            else:
                decrypted_message = raw_message
        elif ext == '.wav':
            raw_message = extract_from_audio(file_path)
            if password:
                decrypted_message = extract_from_audio(file_path, password)
            else:
                decrypted_message = raw_message
        
        if raw_message:
            # Show encrypted message first if password was used
            if password and raw_message != decrypted_message:
                print(f"\n\033[93mEncrypted message:\033[0m")
                print(f"\033[96m{raw_message}\033[0m")
                
                reveal_option = input("\nReveal decrypted message? (y/n): ").strip().lower()
                if reveal_option == 'y':
                    print(f"\n\033[92mDecrypted message:\033[0m")
                    print(f"\033[96m{decrypted_message}\033[0m")
                    message = decrypted_message
                else:
                    message = raw_message
            else:
                print(f"\n\033[92mExtracted message:\033[0m")
                print(f"\033[96m{decrypted_message}\033[0m")
                message = decrypted_message
            
            save_option = input("\nSave to file? (y/n): ").strip().lower()
            if save_option == 'y':
                # Create extracted_messages folder if it doesn't exist
                output_dir = "extracted_messages"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                output_name = input("Enter output filename (without extension): ").strip()
                output_file = os.path.join(output_dir, output_name + ".txt")
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(message)
                print(f"\033[92mMessage saved to {output_file}\033[0m")
        else:
            print("\033[91mFailed to extract message. Check password or file integrity.\033[0m")
            
    except Exception as e:
        print(f"\033[91mError: {str(e)}\033[0m")

def main():
    """Main program loop."""
    while True:
        print_logo()
        print("\n\033[96m=== MAIN MENU ===\033[0m")
        print("1. Hide Me")
        print("2. Reveal Me")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            hide_menu()
        elif choice == '2':
            reveal_menu()
        elif choice == '3':
            print("\n\033[93mThank you for using GhostVault! 👻\033[0m")
            sys.exit(0)
        else:
            print("\033[91mInvalid choice! Please select 1, 2, or 3.\033[0m")
        
        input("\nPress Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[93mGoodbye! 👻\033[0m")
        sys.exit(0)