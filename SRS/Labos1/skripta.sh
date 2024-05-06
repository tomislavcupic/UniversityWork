#!/bin/bash

# Check if required modules are installed
echo "Checking for required Python modules..."
if python3 -c "import Crypto"; then
    echo "Crypto module is already installed."
else
    echo "Installing Crypto module..."
    python3 -m pip install pycryptodome
fi


# Compile Python code
python3 -m py_compile labos.py

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful."
else
    echo "Compilation failed. Exiting."
    exit 1
fi
# Initialize password manager
echo "Initializing password manager..."
python3 labos.py init ja123

# Store passwords
echo "Storing passwords..."
python3 labos.py put ja123 test.com test123
python3 labos.py put ja123 example.com example123

# Retrieve passwords
echo "Retrieving passwords..."
python3 labos.py get ja123 test.com
python3 labos.py get ja123 example.com
python3 labos.py get ja123 non-existent-address

echo "Script execution completed."
