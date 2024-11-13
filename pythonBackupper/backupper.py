import os
import zipfile
import tarfile
import sys
import shutil


def usage():
    print(f"Usage: {os.path.basename(__file__)} [options] [path]")
    print("Manages simple backups of a folder.")
    print("With no path, it will archive the current working directory.")
    print("Options:")
    print("  -c, --create   Creates an archive of the desired directory, inside the directory.")
    print("  -x, --extract  Extracts the content of the archive in the directory.")
    print("  -d, --delete   Deletes the archive of the current directory.")
    print("  -f, --format   Specifies the archive formato: zip (dfault) or tar.")
    print("  -h, --help     Shows this help.")

def create_archive(path=".",format="zip"):
    if path == ".":
        output_zip = f"{os.path.basename(os.getcwd())}.{format}"
    else:
        output_zip = os.path.join(path, f"{os.path.basename(path)}.{format}")
        
    if os.path.isfile(output_zip):
        print(f"{output_zip} already exists.")
        sys.exit(1)

    if format == "zip":
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(path):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), path))
        os.chmod(output_zip, 0o444) # 444 only read
    elif format == "tar":
        with tarfile.open(output_zip, 'w') as tarf:
            tarf.add(path, arcname=os.path.basename(path))
        os.chmod(output_zip, 0o444)
    else:
        print("Unsoported format. Use 'zip' or 'tar' please.")
        sys.exit(1)   

def extract_archive(extract_to=".", format="zip"):
    output_zip = f"{os.path.basename(os.getcwd())}.{format}"
    
    if os.path.isfile(output_zip):
        try:
            # Modify the extraction directory name to avoid conflict with the ZIP file name
            if extract_to == ".":
                extract_to = os.path.basename(os.getcwd()) + "_extracted"
            elif extract_to == os.path.basename(os.getcwd()):
                extract_to += "_extracted"
 
            # Create the extraction directory if it doesn't exist
            if not os.path.exists(extract_to):
                print(f"Creating directory: {extract_to}")
                os.makedirs(extract_to)
            else:
                print(f"Directory already exists: {extract_to}") #qui logica per richiedere

            if format == "zip":
                with zipfile.ZipFile(output_zip, 'r') as zipf:
                    zipf.extractall(path=extract_to)  # extract_to is the directory where the files will be extracted 
                    extracted_files = zipf.namelist()
                    print(f"Extracted files to {extract_to}:")
                    for file in extracted_files:
                        print(file)
            elif format == "tar":
                with tarfile.open(output_zip, 'r') as tarf:
                    tarf.extractall(path=extract_to)
                    extracted_files = tarf.getnames()
                    print(f"Extracted files to {extract_to}:")
                    for file in extracted_files:
                        print(file)
        except Exception as e:
            print(f"An error occurred during extraction: {e}")
    else:
        print(f"No {output_zip} to extract.")
        sys.exit(2)
    
def delete_archive(format="zip"):
    output_zip = f"{os.path.basename(os.getcwd())}.{format}"

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
    format = "zip" #default
    path = "."
    if len(sys.argv) > 3 and (sys.argv[2] == "-f" or sys.argv[2] == "--format"): # caso no path passato
        if sys.argv[3] == "zip" or sys.argv[3] == "tar":
            format = sys.argv[3]
    elif len(sys.argv) > 3:
        path = sys.argv[2]
        if len(sys.argv) > 3 and (sys.argv[-2] == "-f" or sys.argv[-2] == "--format"):
            format = sys.argv[-1]

    if command in ("-c", "--create"):
        create_archive(path, format)
    elif command in ("-x", "--extract"):
        extract_archive(path,format) # Pass the path argument to specify the extraction directory
    elif command in ("-d", "--delete"):
        delete_archive(format)
    elif command in ("-h", "--help"):
        usage()
    else:
        usage()
        sys.exit(4)