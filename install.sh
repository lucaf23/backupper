#!/bin/sh

set -e

if [ $USER = "root" ]; then

    # Root installation

    dest_folder="/usr/local/bin"
    program="$dest_folder/backupper"

    if [ -f "$program" ] || [ -L "$program" ]; then
        rm "$program"
        echo "Deleting existing $program"
    fi

    chmod +x backupper.sh

    cp "$(pwd)/backupper.sh" "$program"
    echo "Copying the program to $dest_folder"

    backupper -h

    echo "Installation completed."

else

    # Non root installation

    dest_folder="$HOME/.local/scripts"
    program="$dest_folder/backupper"

    echo "Warning! You're running this script as non root user."
    echo "The program will be installed in $dest_folder, and your .zshrc and/or .bashrc will be updadet with the export of this new PATH."
    echo "Continue the installation? [y|n]"

    while [ 1 ]; do
        read res
        case $res in
        y)
            break
        ;;
        n)
            exit 0
        ;;
        *)
            echo "Type 'y' or 'n'."
        ;;
        esac
    done

    if [ ! -d "$dest_folder" ]; then
        mkdir -p "$dest_folder"
        echo "Creating $dest_folder"
    else
        if [ -f "$program" ] || [ -L "$program" ]; then
            rm "$program"
            echo "Deleting existing $program"
        fi
    fi

    chmod +x backupper.sh

    cp "$(pwd)/backupper.sh" "$program"
    echo "Copying the program to $dest_folder"

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

fi


