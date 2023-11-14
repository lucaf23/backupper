#!/bin/sh

set -e

dest_folder="$HOME/.local/scripts"
program="$dest_folder/backupper"

if [ ! -d "$dest_folder" ]; then
    mkdir -p "$dest_folder"
    echo "Creating $dest_folder"
else
    if [ -f "$program" ] || [ -L "$program" ]; then
        rm "$program"
        echo "Deleting existing $program"
    fi
fi

chmod u+x backupper.sh

ln -s "$(pwd)/backupper.sh" "$program"
echo "Linking the program to $dest_folder"

export PATH="$PATH:$dest_folder"

backupper -h

if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "export PATH=\"\$PATH:$dest_folder\"" "$HOME/.bashrc"; then
        echo "export PATH=\"\$PATH:$dest_folder\"" >> "$HOME/.bashrc"
        echo "exporting PATH to ~/.bashrc"
    else
        echo "PATH export statement already exists in ~/.bashrc"
    fi
fi

if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "export PATH=\"\$PATH:$dest_folder\"" "$HOME/.zshrc"; then
        echo "export PATH=\"\$PATH:$dest_folder\"" >> "$HOME/.zshrc"
        echo "exporting PATH to ~/.zshrc"
    else
        echo "PATH export statement already exists in ~/.zshrc"
    fi
fi

echo "Installation completed. Run 'source ~.bashrc' or 'source ~.zshrc' to update your configuration."

