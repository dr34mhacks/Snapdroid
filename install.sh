#!/bin/bash

# Install SnapDroid package
echo "Installing SnapDroid..."
pip install -e .

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "SnapDroid installed successfully!"
    echo "You can now run 'snapdroid' from anywhere."
    echo ""
    echo "Try running 'snapdroid --examples' to see usage examples."
else
    echo "Installation failed. Please check the error messages above."
fi