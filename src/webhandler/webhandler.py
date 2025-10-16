''' Module to setup and startup webdriver '''
import os
import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from helpers.constants import CONFIGS, WAYPATH, WAITSEC, BASE_FOLDER
from helpers.dialogator import show_popup_error

class ElementNotFoundException(Exception):
    ''' Custon exception to indicate when element is not found '''

BY = {
    '#': By.ID,
    '/': By.XPATH,
    '.': By.CLASS_NAME
}

class WebHandler:
    ''' Class to Wrap webdriver '''
    def __init__(self, siteurl: str) -> None:
        if not siteurl:
            error_message = 'A argumento `siteurl` não foi definido!'
            show_popup_error(error_message)
            raise ValueError(error_message)
        chromepath = CONFIGS.get('GCHROME', '')
        temppath = CONFIGS.get('TMPPATH', os.path.join(BASE_FOLDER, 'tmp'))
        if not chromepath:
            error_message = 'A configuração "GCHROME" não foi definida!'
            show_popup_error(error_message)
            raise ValueError(error_message)
        driverpath = os.path.join(BASE_FOLDER, 'chromedriver-win64', 'chromedriver.exe')
        if not os.path.exists(driverpath):
            error_message = f'O programa "{driverpath}" não está acessível!'
            show_popup_error(error_message)
            raise FileNotFoundError(error_message)
        service = Service(executable_path=driverpath)
        options = webdriver.ChromeOptions()
        options.binary_location = chromepath
        options.add_argument(f'--app={siteurl}')
        options.add_argument(f'--user-data-dir={temppath}')
        self.driver = webdriver.Chrome(service=service, options=options)
        login = str(CONFIGS.get('USUARIO', ''))
        senha = str(CONFIGS.get('PALAVRA', ''))
        if not login or not senha:
            error_message = 'A configuração "USUARIO" ou "PALAVRA" não foi definida!'
            show_popup_error(error_message)
            raise ValueError(error_message)
        parsed = urlparse(siteurl)
        siteurl = f"{parsed.scheme}://{login}:{senha}@{parsed.hostname}{parsed.path}{parsed.fragment}"
        self.driver.get(siteurl)
        self.driver.maximize_window()
    def get_elements(self, pathname: str, timeout: str) -> list[WebElement] | None:
        ''' Function to get a list of WebElements '''
        # Example 1: /html/body/main/form
        # Will be By.XPATH and '/html/body/main/form'
        # Example 2: #form-item
        # Will be By.CLASS_NAME and 'form-item'
        # Example 3: .form-id
        # Will be By.ID and 'form-id'
        pathvalue = WAYPATH.get(pathname, '')
        if not pathvalue:
            error_message = f'A caminho {pathname} não foi encontrado na configuração!'
            show_popup_error(error_message)
            raise ValueError(error_message)
        bytype = BY.get(pathvalue[:1], '')
        if not bytype:
            error_message = f'O tipo do caminho {pathname} não pode ser definido!'
            show_popup_error(error_message)
            raise ValueError(error_message)
        byvalue = pathvalue[1:] if bytype != By.XPATH else pathvalue
        seconds = WAITSEC.get(timeout, 0)
        expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        while True:
            #try:
            elements = self.driver.find_elements(bytype, byvalue)
            if elements:
                return elements
            #except:
            #    pass
            if datetime.datetime.now() > expiration_time:
                return None
    def get_element(self,
            pathname: str,
            timeout: str,
            replace_text1: int | None = None,
            replace_text2: int | None = None
        ) -> WebElement:
        ''' Function to get a single WebElement '''
        if replace_text1:
            pathname = pathname.replace('?', str(replace_text1))
        if replace_text2:
            pathname = pathname.replace('¿', str(replace_text2))
        elements = self.get_elements(pathname, timeout)
        if not elements:
            error_message = f'O elemento {pathname} não foi encontrado!'
            show_popup_error(error_message)
            raise ElementNotFoundException(error_message)
        return elements[0]
    def select_option(self, element: WebElement, value: str) -> None:
        ''' Function to wrap change select element value '''
        element.find_element(By.XPATH, f'.//option[value="{value}"]').click()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
