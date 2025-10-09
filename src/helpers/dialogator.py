''' Module to wrap logger, console and interface messages '''
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from tkinter import messagebox
from .constants import BASE_FOLDER, APPNAME, DEV_ENV

logger = logging.getLogger(APPNAME)
logspath = os.path.join(BASE_FOLDER, 'log')
if not os.path.exists(logspath):
    os.mkdir(logspath)
logspath = os.path.join(logspath, APPNAME + '.log')
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.DEBUG,
    handlers = [
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(filename=logspath, maxBytes=1000000, backupCount=5)
    ]
)

def show_popup_error(message: str, show: bool = True) -> None:
    ''' Function to show a popup message about erros '''
    logger.error(message)
    if show:
        messagebox.showerror('Erro!', message=message)

def show_popup_info(message: str, show: bool = True) -> None:
    ''' Function to show a popup message about info '''
    logger.info(message)
    if show:
        messagebox.showinfo('Info!', message=message)

def show_popup_debug(message: str) -> None:
    ''' Function to show a popup message about debug '''
    logger.debug(message)
    if DEV_ENV:
        messagebox.showinfo('Debug!', message=message)
