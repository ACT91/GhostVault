#!/usr/bin/env python3
"""Simple test script for GhostVault functionality."""

import os
import sys
from PIL import Image
import numpy as np
import wave

def create_test_image():
    """Create a simple test image."""
    img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save("test_image.png")
    print("Created test_image.png")

def create_test_audio():
    """Create a simple test audio file."""
    sample_rate = 44100
    duration = 1  # 1 second
    samples = np.random.randint(-32768, 32767, sample_rate * duration, dtype=np.int16)
    
    with wave.open("test_audio.wav", 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())
    
    print("Created test_audio.wav")

if __name__ == "__main__":
    print("Creating test files for GhostVault...")
    create_test_image()
    create_test_audio()
    print("\nTest files created! You can now test GhostVault with:")
    print("- test_image.png")
    print("- test_audio.wav")
    print("\nRun: python ghostvault.py")