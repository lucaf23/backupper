#!/bin/sh

set -e

if [ $USER = "root" ]; then
    dest_folder="/usr/local/bin"
    program="$dest_folder/backupper"
else
    echo "Warning: you are running this script as non root."
    echo "This will only remove (if present) the .local installation."
    echo "'sudo sh $0' for the root uninstall."
    dest_folder="$HOME/.local/scripts"
    program="$dest_folder/backupper"
fi

if [ -f "$program" ] || [ -L "$program" ]; then
    rm "$program"
    echo "Deleting existing $program"
else
    echo "Backupper isn't installed."
fi
