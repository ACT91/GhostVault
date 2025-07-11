#!/usr/bin/env python3
"""
GhostVault - Text-based Steganography Tool
Created by ACT91
GitHub: https://github.com/ACT91
"""

import click
import os
from steg.image_steg import hide_in_image, extract_from_image
from steg.audio_steg import hide_in_audio, extract_from_audio
from utils.validator import validate_file, check_capacity

@click.group()
def cli():
    """GhostVault - Text-based steganography tool by ACT91"""
    pass

@cli.command()
@click.option('--file', '-f', required=True, help='Input file path')
@click.option('--message', '-m', required=True, help='Secret message to hide')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--password', '-p', help='Password for encryption (optional)')
def hide(file, message, output, password):
    """Hide a secret message in an image or audio file."""
    try:
        if not validate_file(file):
            click.echo(f"Error: Invalid or unsupported file: {file}")
            return
        
        if not check_capacity(file, message):
            click.echo("Error: Message too long for the cover file")
            return
        
        file_ext = os.path.splitext(file)[1].lower()
        
        if file_ext in ['.png', '.jpg', '.jpeg']:
            hide_in_image(file, message, output, password)
        elif file_ext in ['.wav']:
            hide_in_audio(file, message, output, password)
        else:
            click.echo(f"Error: Unsupported file format: {file_ext}")
            return
        
        click.echo(f"Message successfully hidden in {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option('--file', '-f', required=True, help='File to extract message from')
@click.option('--password', '-p', help='Password for decryption (optional)')
@click.option('--output', '-o', help='Save extracted message to file (optional)')
def extract(file, password, output):
    """Extract a hidden message from an image or audio file."""
    try:
        if not validate_file(file):
            click.echo(f"Error: Invalid or unsupported file: {file}")
            return
        
        file_ext = os.path.splitext(file)[1].lower()
        message = None
        
        if file_ext in ['.png', '.jpg', '.jpeg']:
            message = extract_from_image(file, password)
        elif file_ext in ['.wav']:
            message = extract_from_audio(file, password)
        else:
            click.echo(f"Error: Unsupported file format: {file_ext}")
            return
        
        if message:
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(message)
                click.echo(f"Message extracted and saved to {output}")
            else:
                click.echo(f"Extracted message: {message}")
        else:
            click.echo("No hidden message found or incorrect password")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    cli()