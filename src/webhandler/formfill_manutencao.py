''' Module to handle with fill `manutencao` Sharepoint '''
import pandas
from .webhandler import WebHandler

def formfill_manutencao(infolist: pandas.DataFrame, filelist: list[str]) -> None:
    ''' Function to handle with fill `manutencao` Sharepoint '''
