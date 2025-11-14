# SharePoint data entry automation and information extraction program

> This program was created to meet a specific layout and is not intended to serve other purposes!

## Installation

The program does not require a specific installation procedure. Simply extract the file created in the releases section to any folder, preferably on the desktop for easy access.

## Configuration

Fill in the `mos_bot.conf` configuration file with the necessary information. There are instructions in Portuguese for each setting within the file itself. All paths entered must be absolute.

## Usage

The program works in two modes: `INSERIR` or `EXTRAIR`; according to the `OPERATION` setting in the `mos_bot.conf` file.

### Insertion Mode (INSERIR)

In this mode, the program retrieves information from the file `consulta_medicao_completa.xlsx`, which must be up-to-date in the program's installation folder. It will use this file to retrieve the necessary information for populating SharePoint.

After loading the spreadsheet into memory, the program will check for files and folders in the folder indicated in the `UPOPATH` setting. It will navigate until it finds the folder hierarchy that matches the depth defined in the `PROFUNDIDADE` setting.

The folder/file name will be used to retrieve the information related to the document(s). If the program finds the information, it will populate SharePoint; otherwise, it will ignore the folder/file and search for the next one.

### Extraction Mode (EXTRAIR)

In this mode, you only need to start the program, and it will authenticate, load the measurements page, and export a report to the folder indicated in the `ODLPATH` configuration.

The report is exported as a CSV file, and for correct viewing in Excel, it must be imported using data analysis tools (Microsoft PowerQuery).

## Development

To create an executable, follow the steps below:

1. Check the installation and versions of the requirements:

    ```sh
    # Checks the Python installation and version
    # Version 3.13.7 or higher
    python --version
    # Checks the Pip installation and version
    # Version 25.2 or higher
    pip --version
    ```

    > The target operating system for this project is Windows.

2. It is recommended to create and activate the virtual environment to install the dependencies:

    ```sh
    # Creates the virtual environment
    python -m venv venv
    # Activates the virtual environment
    source venv/Scripts/activate
    # Installs the dependencies
    pip install -r requirements.txt
    ```

## Distribution

1. Use `PyInstaller` to create an executable:

    ```sh
    pyinstaller --icon appicon.ico --hidden-import lxml --onefile src/mos_bot.py
    ```

    > The executable will be saved in the `dist` folder, in the project's root directory.

2. Pack all related files to zip file:

    ```sh
    zip -j dist/MOS_BOT.zip readme.md dist/mos_bot.exe src/mos_bot.conf src/mos_bot.path
    cd src && zip -r ../dist/MOS_BOT.zip chromedriver-win64 && cd ..
    ```
