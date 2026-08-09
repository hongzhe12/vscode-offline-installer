#!/bin/bash

pyinstaller \
    --onefile \
    --name vscode-installer \
    --add-data "packages:packages" \
    install.py