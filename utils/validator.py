import os
from PIL import Image
import wave

def validate_file(file_path):
    """Validate if file exists and is supported format."""
    if not os.path.exists(file_path):
        return False
    
    ext = os.path.splitext(file_path)[1].lower()
    supported_formats = ['.png', '.jpg', '.jpeg', '.wav']
    
    return ext in supported_formats

def check_capacity(file_path, message):
    """Check if file can hold the message."""
    ext = os.path.splitext(file_path)[1].lower()
    message_bits = len(message + "###END###") * 8
    
    try:
        if ext in ['.png', '.jpg', '.jpeg']:
            img = Image.open(file_path)
            total_pixels = img.width * img.height * len(img.getbands())
            return message_bits <= total_pixels
        
        elif ext == '.wav':
            with wave.open(file_path, 'rb') as audio:
                frames = audio.getnframes()
                return message_bits <= frames
        
    except Exception:
        return False
    
    return False