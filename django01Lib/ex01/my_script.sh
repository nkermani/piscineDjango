#!/usr/bin/env bash

if ! pip --version > /dev/null 2>&1; then
    echo "pip is not installed. Please install pip to proceed."
    exit 1
fi

# Upgrade pip and setuptools to support modern build systems
# pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Check if local_lib directory exists
if [ ! -d "local_lib" ]; then
    mkdir local_lib
fi

# Check if path.py is already installed and remove it
if [ -d "local_lib/path" ] || [ -d "local_lib/path.py" ]; then
    rm -rf local_lib/path*
fi

# Install development version of path.py from GitHub
pip install git+https://github.com/jaraco/path.git --target=local_lib --upgrade > path_install.log 2>&1

if [ $? -eq 0 ]; then
    python3 my_program.py
else
    echo "Failed to install path.py. Check path_install.log for details."
    exit 1
fi
