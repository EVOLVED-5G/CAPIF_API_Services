#!/bin/bash
echo "Installing basic software related with robotFramework"
source /opt/venv/bin/activate; 
pip install --upgrade pip
pip install --upgrade robotframework; 
pip install --upgrade robotframework-seleniumlibrary; 
pip install --upgrade webdrivermanager; 
webdrivermanager firefox chrome --linkpath /usr/local/bin;
pip install -r $1 
echo "Robot framework installed"
