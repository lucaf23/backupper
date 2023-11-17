# Backupper
A simple tool to manage backups of single folders.

## Usage
```bash
Usage: backupper [options] [path]
Manages simple backups of a folder.
With no path, it will be archived the current working directory.
Options:
  -c, --create   Creates an archive of the desired directory, inside the directory.
  -x, --extract  Extract the content of the archive in the directory.
  -d, --delete   Deletes the archive of the current directory.
  -h, --help     Shows this help. 
 ```

## Installation
The installation process installs the program as a copy of the script in /usr/local/bin.

Clone this repository:

```bash
git clone https://github.com/alessandrogilli/backupper.git
```

Enter the project directory:
```bash
cd backupper
```

Run the install script as root:
```bash
sudo sh ./install.sh
```

Run the program:
```bash
backupper
```

### Non root installation

If you prefer to install the program without root permissions, the installation process will copy the script in a new "script" directory inside your ~/.local folder. It also auto updates .bashrc and .zshrc files with the new $PATH variable.

Run the install script:
```bash
sh ./install.sh
```

Open a new shell or type:
```bash
source ~/.bashrc
```

or, if you are using zsh:
```bash
source ~/.zshrc
```

Finally, you can find backupper installed, typing:
```bash
backupper
```


