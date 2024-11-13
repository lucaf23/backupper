import os
import zipfile
import tarfile
import sys
from datetime import datetime

def usage():
    print(f"Usage: {os.path.basename(__file__)} [options] [path]")
    print("Manages simple backups of a folder.")
    print("With no path, it will archive the current working directory.")
    print("Options:")
    print("  -c, --create   Creates an archive of the desired directory, inside the directory.")
    print("  -x, --extract  Extracts the content of the archive in the directory.")
    print("                 Actions for extract:")
    print("                   1: Extracts from current directory archive.")
    print("                   2: Extracts from specified archive name.zip or name.tar present in current directory.")
    print("                   3: Extracts from specified archive name.zip/tar to specified directory.")
    print("  -d, --delete   Deletes the archive of the current directory.")
    print("  -f, --format   Specifies the archive format: zip (default) or tar.")
    print("  -h, --help     Shows this help.")

def create_archive(path=".", format="zip"):
    # Determina il percorso dell'archivio di output
    output_zip = os.path.join(path, f"{os.path.basename(os.getcwd())}.{format}")

    # Verifica se l'archivio esiste già
    if os.path.isfile(output_zip):
        print(f"{output_zip} already exists.")
        sys.exit(1)

    # Crea l'archivio in base al formato specificato
    if format == "zip":
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("."):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), "."))
        os.chmod(output_zip, 0o444)  # 444 solo lettura
    elif format == "tar":
        with tarfile.open(output_zip, 'w') as tarf:
            tarf.add(".", arcname=os.path.basename(os.getcwd()))
        os.chmod(output_zip, 0o444)
    else:
        print("Unsupported format. Use 'zip' or 'tar' please.")
        sys.exit(1)

def extract_archive(action, path1=".", path2=None, format=None):
    if format is None:
        format = os.path.splitext(path1)[1][1:]

    if action == 1:   # Opzione 1: Estrae il contenuto dal file di archivio nella directory corrente
        output_zip = f"{os.path.basename(os.getcwd())}.{format}"
        extract_to = os.path.basename(os.getcwd()) + "_extracted"
    elif action == 2: # Opzione 2: Estrae il contenuto dal file di archivio specificato nella directory corrente
        output_zip = os.path.join(os.getcwd(), path1)
        current_date = datetime.now().strftime("%Y%m%d")
        extract_to = os.path.splitext(path1)[0] + f"_extracted_{current_date}"
    elif action == 3: # Opzione 3: Estrae il contenuto dal file di archivio specificato in una nuova directory 
        output_zip = os.path.join(os.getcwd(), path1)
        current_date = datetime.now().strftime("%Y%m%d")
        extract_to = os.path.join(path2, os.path.splitext(os.path.basename(path1))[0] + f"_extracted_{current_date}")
    else:
        print("Invalid action specified.")
        sys.exit(1)

    if os.path.isfile(output_zip):
        try:
            if not os.path.exists(extract_to):
                print(f"Creating directory: {extract_to}")
                os.makedirs(extract_to)
            else:
                print(f"Directory already exists: {extract_to}")

            if format == "zip":
                with zipfile.ZipFile(output_zip, 'r') as zipf:
                    zipf.extractall(path=extract_to)
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
            else:
                print("Unsupported format. Use 'zip' or 'tar' please.")
                sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    else:
        print(f"No archive found with the name {output_zip}.")
        sys.exit(1)
    
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
    format = None #default
    path = "."
    action = 1
    path2 = None

    if len(sys.argv) > 3 and (sys.argv[2] == "-f" or sys.argv[2] == "--format"): # caso no path passato
        if sys.argv[3] == "zip" or sys.argv[3] == "tar":
            format = sys.argv[3]

    elif len(sys.argv) > 2:
        path = sys.argv[2]
        action = 2
        if len(sys.argv) >= 4 and (sys.argv[1] == "-x" or sys.argv[1] == "--extract") and sys.argv[3] != "-f":
            action = 3
            path2 = sys.argv[3]

    if len(sys.argv) > 3 and (sys.argv[-2] == "-f" or sys.argv[-2] == "--format"):
        format = sys.argv[-1]


    if command in ("-c", "--create"):
        create_archive(path, format if format else "zip")
    elif command in ("-x", "--extract"):
        extract_archive(action,path,path2,format) # Pass the path argument to specify the extraction directory
    elif command in ("-d", "--delete"):
        delete_archive(format if format else "zip")
    elif command in ("-h", "--help"):
        usage()
    else:
        usage()
        sys.exit(4)