import os
import zipfile
import sys


def usage():
    print(f"Usage: {os.path.basename(__file__)} [options] [path]")
    print("Manages simple backups of a folder.")
    print("With no path, it will archive the current working directory.")
    print("Options:")
    print("  -c, --create   Creates an archive of the desired directory, inside the directory.")
    print("  -x, --extract  Extracts the content of the archive in the directory.")
    print("  -d, --delete   Deletes the archive of the current directory.")
    print("  -h, --help     Shows this help.")

def create_archive(path="."):
    output_zip = f"{os.path.basename(os.getcwd())}.zip"
    if not os.path.isfile(output_zip):
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(path):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), path))
        os.chmod(output_zip, 0o444)
    else:
        print(f"{output_zip} already exists.")
        sys.exit(1)

def extract_archive():
    output_zip = f"{os.path.basename(os.getcwd())}.zip"
    if os.path.isfile(output_zip):
        with zipfile.ZipFile(output_zip, 'r') as zipf:
            zipf.extractall()
        os.remove(output_zip)
    else:
        print(f"No {output_zip} to extract.")
        sys.exit(2)

def delete_archive():
    output_zip = f"{os.path.basename(os.getcwd())}.zip"
    if os.path.isfile(output_zip):
        os.remove(output_zip)
        print(f"{output_zip} deleted.")
    else:
        print(f"No {output_zip} to delete.")
        sys.exit(3)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(4)

    command = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else "."

    if command in ("-c", "--create"):
        create_archive(path)
    elif command in ("-x", "--extract"):
        extract_archive()
    elif command in ("-d", "--delete"):
        delete_archive()
    elif command in ("-h", "--help"):
        usage()
    else:
        usage()
        sys.exit(4)