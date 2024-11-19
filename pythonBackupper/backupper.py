import os
import zipfile
import tarfile
import sys
import pyzipper
import getpass
from datetime import datetime
import glob

def usage():
    print(f"Usage: {os.path.basename(__file__)} [options] [path]")
    print("Manages simple backups of a folder.")
    print("With no path, it will archive the current working directory.")
    print("Options:")
    print("  -c, --create       Creates an archive of the desired directory, inside the directory or in a new one if specified.")
    print("  -c [path] -f tar   Creates an tar archive of the current directory, in the specified directory.")
    print("  -x, --extract      Extracts the content of the archive in the directory.")
    print("                     Actions for extract:")
    print("                             1: Extracts from current directory archive.")
    print("  -x [archive_name.format]   2: Extracts from specified archive name.zip or name.tar present in current directory.")
    print("  -x [name] [path]           3: Extracts from specified archive name.zip/tar to specified directory 'path'.")
    print("  -d, --delete       Deletes the archive of the current directory. Can specify the format.")
    print("  -f, --format       Specifies the archive format: zip (default) or tar.")
    print("  -h, --help         Shows this help and exit.") 


def create_zip_archive(path, output_name , passphrase=None):
    if passphrase:
        with pyzipper.AESZipFile(output_name, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(passphrase.encode())  # Convert the passphrase to bytes
            for root, dirs, files in os.walk("."):
                for file in files:
                    zf.write(os.path.join(root, file),
                             os.path.relpath(os.path.join(root, file), "."))
        print(f"ZIP archive {output_name} created with passoword encryption.")
    else:
        with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk("."):
                for file in files:
                    zf.write(os.path.join(root, file),
                             os.path.relpath(os.path.join(root, file), "."))
        print(f"ZIP archive {output_name} created.")

def create_archive(path=".", format="zip", passphrase=None):
    # Determina il percorso dell'archivio di output
    current_date = datetime.now().strftime("%Y%m%d")

    output_zip = os.path.join(path, f"{os.path.basename(os.getcwd())}_{current_date}.{format}")

    # Verifica se l'archivio esiste già
    if os.path.isfile(output_zip):
        response = input(f"{output_zip} already exists. Overwrite? (y/n): ")
        if response.lower() != "y":
            print("Operation Aborted!")
            sys.exit(1)

    # Crea l'archivio in base al formato specificato
    if format == "zip":
        create_zip_archive(path, output_zip, passphrase)
        #os.chmod(output_zip, 0o444)  # 444 solo lettura
    elif format == "tar":
        if passphrase:
            print("Sorry, Tar format does not support encryption.")
            sys.exit(1)
        with tarfile.open(output_zip, 'w') as tarf:
            tarf.add(".", arcname=os.path.basename(os.getcwd()))
        os.chmod(output_zip, 0o444)
    else:
        print("Unsupported format. Use 'zip' or 'tar' please.")
        sys.exit(1)

def trovaArchivioRecente(format="zip"):
    #trova archivio più recente
    base_name = os.path.basename(os.getcwd())
    pattern = f"{base_name}_*.{format}"
    files = glob.glob(pattern)
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def trovaArchivioVecchio(format="zip"):
    # Trova l'archivio più vecchio
    base_name = os.path.basename(os.getcwd())
    pattern = f"{base_name}_*.{format}"
    files = glob.glob(pattern)
    if not files:
        return None
    oldest_file = min(files, key=os.path.getmtime)
    return oldest_file

def extract_archive(action, path1=".", path2=None, format=None):
    if format is None:
        print("Format not specified. Please specify the format of the archive using -f tar/zip.")
        sys.exit(1)
        #format = os.path.splitext(path1)[1][1:]
  
    if action == 1:   # Opzione 1: Estrae il contenuto dal file di archivio nella directory corrente
        archive_path = trovaArchivioRecente(format)
        if not archive_path:
            print(f"Nessun archivio.{format}  trovato nella directory corrente.")
            sys.exit(1)
        #output_zip = f"{os.path.basename(os.getcwd())}.{format}"
        #output_zip = os.path.join(os.getcwd(), archive_path)
        extract_to = os.path.splitext(archive_path)[0] + "_extracted"
        print(f"Extracting archive {archive_path} to {extract_to} with format {format}")
        output_zip = archive_path
    elif action == 2: # Opzione 2: Estrae il contenuto dal file di archivio specificato nella directory corrente
        output_zip = os.path.join(os.getcwd(), path1)
        extract_to = os.path.splitext(path1)[0] + f"_extracted"
    elif action == 3: # Opzione 3: Estrae il contenuto dal file di archivio specificato in una nuova directory 
        output_zip = os.path.join(os.getcwd(), path1)
        extract_to = os.path.join(path2, os.path.splitext(os.path.basename(path1))[0] + f"_extracted")
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
                #check password all' utente
                try:
                    with pyzipper.AESZipFile(output_zip) as zf:
                        zf.extractall(path=extract_to)
                        extracted_files = zf.namelist()
                        print(f"Extracted files to {extract_to}:")
                        for file in extracted_files:
                            print(file)
                except RuntimeError as e:
                    if 'requires a password' in str(e).lower():
                        passphrase = getpass.getpass("Enter the passphrase to decrypt the archive: ")
                        try:
                            with pyzipper.AESZipFile(output_zip) as zf:
                                zf.setpassword(passphrase.encode())
                                zf.extractall(path=extract_to)
                                extracted_files = zf.namelist()
                                print(f"Extracted files to {extract_to}:")
                                for file in extracted_files:
                                    print(file)
                        except RuntimeError as e:
                            print("Password incorrect. Extraction failed.")
                            sys.exit(2)
                    else:
                        print(f"An error occurred: {e}")
                        sys.exit(2)
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
            if 'requires a password' not in str(e).lower():
                sys.exit(1)
    else:
        print(f"No archive found with the name {output_zip}.")
        sys.exit(1)
    
def delete_archive(format="zip"):
    #output_zip = f"{os.path.basename(os.getcwd())}.{format}"
    archive_path = trovaArchivioVecchio(format)
    if not archive_path:
        print(f"Nessun archivio nella directory trovato con formato: {format}.")
        sys.exit(1)

    if os.path.isfile(archive_path):
        os.remove(archive_path)
        print(f"{archive_path} eliminato.")
    else:
        print(f"No archive found with the name {archive_path}.")
        sys.exit(1)

def cutFormat(path="zip"):
    #estraggo zip o tar da nome file passato
    _, ext = os.path.splitext(path)
    return ext[1:] if ext else ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(3)

    command = sys.argv[1]
    format = None #default
    path = "."
    action = 1
    path2 = None

    #func legge pat.xtz tolgo -f da specificare in -x 
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
        passphrase = getpass.getpass("Enter a password for encryption (leave blank for no encryption): ")
        create_archive(path, format if format else "zip", passphrase)
    elif command in ("-x", "--extract"):
        if(action == 2 | action == 3): #check 
            format = cutFormat(path)
        extract_archive(action,path,path2,format) # Pass the path argument to specify the extraction directory
    elif command in ("-d", "--delete"):
        delete_archive(format if format else "zip")
    elif command in ("-h", "--help"):
        usage()
    else:
        usage()
        sys.exit(3)