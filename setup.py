from setuptools import setup, find_packages

setup(
    name="ghostvault",
    version="1.0.0",
    description="Cross-platform text-based steganography tool",
    packages=find_packages(),
    install_requires=[
        "pillow>=9.0.0",
        "numpy>=1.21.0", 
        "cryptography>=3.4.0",
        "click>=8.0.0"
    ],
    entry_points={
        'console_scripts': [
            'ghostvault=main:cli',
        ],
    },
    python_requires=">=3.7",
)