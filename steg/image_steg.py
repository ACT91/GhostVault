from PIL import Image
import numpy as np
from .crypto import encrypt_message, decrypt_message

def hide_in_image(image_path, message, output_path, password=None):
    """Hide a message in an image using LSB steganography."""
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Encrypt message if password provided
    if password:
        message = encrypt_message(message, password)
    
    # Add delimiter to mark end of message
    message += "###END###"
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Flatten image array for easier manipulation
    flat_img = img_array.flatten()
    
    # Hide message in LSBs
    for i, bit in enumerate(binary_message):
        flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
    
    # Reshape back to original dimensions
    modified_img = flat_img.reshape(img_array.shape)
    
    # Save the modified image
    result_img = Image.fromarray(modified_img.astype(np.uint8))
    result_img.save(output_path)

def extract_from_image(image_path, password=None):
    """Extract a hidden message from an image."""
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Flatten image array
    flat_img = img_array.flatten()
    
    # Extract LSBs
    binary_message = ""
    for pixel in flat_img:
        binary_message += str(pixel & 1)
    
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
        # Try to find any valid message
        if len(message) < 10:  # Too short to be meaningful
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