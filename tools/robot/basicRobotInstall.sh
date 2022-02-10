#!/bin/bash
echo "Installing basic software related with robotFramework"
source /opt/venv/bin/activate; 
pip install --upgrade pip
pip install --upgrade robotframework;
pip install -r $1 
echo "Robot framework installed"
