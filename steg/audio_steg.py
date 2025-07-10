import wave
import numpy as np
from .crypto import encrypt_message, decrypt_message

def hide_in_audio(audio_path, message, output_path, password=None):
    """Hide a message in an audio file using LSB steganography."""
    with wave.open(audio_path, 'rb') as audio:
        frames = audio.readframes(-1)
        sound_data = np.frombuffer(frames, dtype=np.int16)
        params = audio.getparams()
    
    # Encrypt message if password provided
    if password:
        message = encrypt_message(message, password)
    
    # Add delimiter to mark end of message
    message += "###END###"
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Hide message in LSBs of audio samples
    for i, bit in enumerate(binary_message):
        if i < len(sound_data):
            sound_data[i] = (sound_data[i] & 0xFFFE) | int(bit)
    
    # Save modified audio
    with wave.open(output_path, 'wb') as output_audio:
        output_audio.setparams(params)
        output_audio.writeframes(sound_data.tobytes())

def extract_from_audio(audio_path, password=None):
    """Extract a hidden message from an audio file."""
    with wave.open(audio_path, 'rb') as audio:
        frames = audio.readframes(-1)
        sound_data = np.frombuffer(frames, dtype=np.int16)
    
    # Extract LSBs
    binary_message = ""
    for sample in sound_data:
        binary_message += str(sample & 1)
    
    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            try:
                char = chr(int(byte, 2))
                message += char
                
                # Check for end delimiter
                if message.endswith("###END###"):
                    message = message[:-9]  # Remove delimiter
                    break
            except ValueError:
                continue
    
    if not message or not message.endswith("###END###") and "###END###" not in message:
        if len(message) < 10:
            return None
    
    # Clean message if delimiter found
    if "###END###" in message:
        message = message.split("###END###")[0]
    
    # Decrypt message if password provided
    if password and message:
        try:
            message = decrypt_message(message, password)
        except:
            return None
    
    return message if message else None