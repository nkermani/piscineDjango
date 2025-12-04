#!/usr/bin/env bash
pip --version

if ! pip --version > /dev/null 2>&1; then
    echo "pip is not installed. Please install pip to proceed."
    exit 1
fi

python3 -m venv django_venv

source django_venv/bin/activate

pip install -r requirement.txt

pip list

echo "Virtual environment created and packages installed."
echo "To activate the environment, run:"
echo "  source django_venv/bin/activate"
