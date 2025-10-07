''' Module that check updates and apply then '''
import os
import re
import shutil
import zipfile
import requests
from .constants import BASE_FOLDER, CONFIGS
from .executor import execute
from .dialogator import show_popup_info, show_popup_error
from .version import Version

DRIVER_REMOTE = 'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE'

DRIVER_DOWNLOAD = 'https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win64/chromedriver-win64.zip'

class VersionNotFound(Exception):
    ''' Custon exception to indicate that version could not be defined '''

class CannotDownloadUpdate(Exception):
    ''' Custon exception to indicate that update couldn't be download '''

def get_version_from_string_output(result: str) -> Version | None:
    ''' Function to get version number from version string '''
    match = re.search(r'\d+(?:\.\d+)+', result)
    if not match:
        return None
    return Version(match.group())

def googlechrome_get_local_version() -> Version:
    ''' Function to get installed Google Chrome version '''
    chromepath = CONFIGS.get('GCHROME')
    if not chromepath:
        error_message = 'A configuração `GCHROME` não foi definida!'
        show_popup_error(error_message)
        raise ValueError(error_message)
    if not os.path.exists(chromepath):
        error_message = f'O programa "{chromepath}" não está acessível!'
        show_popup_error(error_message)
        raise FileNotFoundError(error_message)
    version = get_version_from_string_output(execute(
        'powershell',
        f'-c "(Get-Item "{chromepath}").VersionInfo.ProductVersion.ToString()"'
    ))
    if not version:
        error_message = 'A versão do navegador GoogleChrome não pode ser obtida!'
        show_popup_error(error_message)
        raise VersionNotFound(error_message)
    return version

def chromedriver_get_local_version() -> Version:
    ''' Function to get installed Chrome Driver version '''
    driverpath = os.path.join(BASE_FOLDER, 'chromedriver-win64', 'chromedriver.exe')
    if not os.path.exists(driverpath):
        return Version(0, 0, 0)
    version = get_version_from_string_output(execute(driverpath, '--version'))
    if not version:
        error_message = 'A versão do ChromeDriver local não pode ser obtida!'
        show_popup_error(error_message)
        raise VersionNotFound(error_message)
    return version

def chromedriver_get_remote_version() -> Version:
    ''' Function to get info about Chrome Driver versions '''
    response = requests.get(DRIVER_REMOTE, timeout=60)
    version = get_version_from_string_output(response.text)
    if not version:
        error_message = 'A versão do ChromeDriver remoto não pode ser obtida!'
        show_popup_error(error_message)
        raise VersionNotFound(error_message)
    return version

def chromedriver_download_newer_version(driver_version: Version) -> None:
    ''' Function to download newer version of Chrome Driver '''
    update_path = os.path.join(BASE_FOLDER, 'chromedriver-win64.zip')
    response = requests.get(DRIVER_DOWNLOAD.format(driver_version=str(driver_version)), timeout=60)
    if not response.ok:
        error_message = 'Não foi possível baixar a atualização!'
        show_popup_error(error_message)
        raise CannotDownloadUpdate(error_message)
    with open(update_path, 'wb') as file:
        file.write(response.content)

def chromedriver_remove_older_version() -> None:
    ''' Function to uninstall previous version '''
    driverpath = os.path.join(BASE_FOLDER, 'chromedriver-win64')
    if os.path.exists(driverpath):
        shutil.rmtree(driverpath)

def chromedriver_install_newer_version() -> None:
    ''' Function to install newer version '''
    update_path = os.path.join(BASE_FOLDER, 'chromedriver-win64.zip')
    if not os.path.exists(update_path):
        error_message = 'O arquivo de atualização não está acessível!'
        show_popup_error(error_message)
        raise CannotDownloadUpdate(error_message)
    # driverpath = os.path.join(BASE_FOLDER, 'chromedriver-win64')
    # if not driverpath:
    #     os.mkdir(driverpath)
    with zipfile.ZipFile(update_path, 'r') as zip_ref:
        zip_ref.extractall(BASE_FOLDER)

def update_chromedriver() -> None:
    ''' Main function to check programs versions and update then '''
    # Verificando as versões do browser e do driver
    show_popup_info('Verificando as versões do browser e do driver...', False)
    chrome_version = googlechrome_get_local_version()
    show_popup_info(f'Chrome major version: {chrome_version}.', False)
    driver_version = chromedriver_get_local_version()
    show_popup_info(f'Driver major version: {driver_version}.', False)
    if driver_version > chrome_version:
        return
    # Verificando atualização do chromedriver
    show_popup_info('Verificando atualização do chromedriver...', False)
    newer_version = chromedriver_get_remote_version()
    show_popup_info(f'Versão do chromedriver no canal STABLE: {newer_version}', False)
    # Atualizando o chromedriver com a nova versão
    show_popup_info('Baixando a nova versão do chromedriver...', False)
    chromedriver_download_newer_version(newer_version)
    show_popup_info('Removendo a versão antiga do chromedriver...', False)
    chromedriver_remove_older_version()
    show_popup_info('Descompactando e instalando a atualização...', False)
    chromedriver_install_newer_version()
    show_popup_info('Atualização do chromedriver foi concluída!', False)
    return
