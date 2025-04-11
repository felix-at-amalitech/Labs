#!/bin/bash

ENV_NAME="${1:-lab-1-env}"

echo "Creating $ENV_NAME virtual environment"

if [ -d "$ENV_NAME" ]; then
  echo "Virtual environment '$ENV_NAME' already exists."
else
  python3 -m venv --upgrade-deps "$ENV_NAME"
  if [ $? -ne 0 ]; then
    echo "Error creating virtual environment '$ENV_NAME'. Exiting."
    exit 1
  fi
fi

if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt"
  "$ENV_NAME/bin/pip" install -r requirements.txt
  if [ $? -ne 0 ]; then
    echo "Error installing requirements. Exiting."
    exit 1
  fi
else
  echo "Warning: requirements.txt not found. Skipping installation."
fi

echo ""
echo "To activate the virtual environment, run:"
echo "  source $ENV_NAME/bin/activate"
echo ""