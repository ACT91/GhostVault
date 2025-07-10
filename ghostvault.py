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
            # Try to detect if it's encrypted (contains non-printable chars)
            is_encrypted = any(ord(c) > 127 or (ord(c) < 32 and c not in '\n\r\t') for c in message[:50])
            return "text", is_encrypted
        return None, None
    except:
        return None, None

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
        print("\033[91mError: Invalid or unsupported file!\033[0m")
        return
    
    message = input("Enter secret message: ").strip()
    
    if not check_capacity(file_path, message):
        print("\033[91mError: Message too long for the cover file!\033[0m")
        return
    
    output_path = input("Enter output file path: ").strip().strip('"')
    
    use_password = input("Use password protection? (y/n): ").strip().lower()
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
    
    if is_encrypted:
        print("\033[93mContent appears to be encrypted.\033[0m")
        password = input("Enter password (or press Enter to try without): ").strip()
        password = password if password else None
    else:
        password = None
    
    print("\n1. Extract Message")
    choice = input("Select option (1): ").strip()
    
    if choice != '1':
        print("\033[91mInvalid choice!\033[0m")
        return
    
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg']:
            message = extract_from_image(file_path, password)
        elif ext == '.wav':
            message = extract_from_audio(file_path, password)
        
        if message:
            print(f"\n\033[92mExtracted message:\033[0m")
            print(f"\033[96m{message}\033[0m")
            
            save_option = input("\nSave to file? (y/n): ").strip().lower()
            if save_option == 'y':
                output_file = input("Enter output filename: ").strip()
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