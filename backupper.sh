#!/bin/bash

set -e

# Function to display usage information
usage() {
    echo "Usage: $(basename $0) [options] [path]"
    echo "Manages simple backups of a folder."
    echo "With no path, it will be archived the current working directory."
    echo "Options:"
    echo "  -c, --create   Creates an archive of the desired directory, inside the directory."
    echo "  -x, --extract  Extract the content of the archive in the directory."
    echo "  -d, --delete   Deletes the archive of the current directory."
    echo "  -h, --help     Shows this help."
}
 
output_zip="$(basename $(pwd)).zip"

# Default value for path
if [ -z "$2" ]; then
    path="."
else
    path=$2
fi

case "$1" in
    -c|--create)
    if [ ! -f $output_zip ]; then
        zip -r -9 $output_zip "$path"
        chmod 444 $output_zip
    else
        echo "$output_zip already exixsts."
        exit 1
    fi
        ;;
    -x|--extract)
    if [ -f $output_zip ]; then
        unzip $output_zip
        rm -rf $output_zip
    else
        echo "No $output_zip to extract."
        exit 2
    fi
        ;;
    -d|--delete)
    if [ -f $output_zip ]; then
        rm -rf $output_zip
        echo "$output_zip deleted."
    else
        echo "No $output_zip to delete."
        exit 3
    fi
        ;;
    -h|--help)
        usage
        ;;
    *)
        usage
        exit 4
        ;;
esac

exit 0