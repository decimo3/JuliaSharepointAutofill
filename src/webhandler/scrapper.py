''' Module to scrapper Sharepoint forms '''
import os
from io import StringIO
from datetime import datetime
from pandas import DataFrame, read_html
from webhandler.webhandler import WebHandler, ElementNotFoundException
from helpers.constants import BASE_FOLDER, CONFIGS

def scrapper_expansao(handler: WebHandler) -> DataFrame:
    ''' Function to scrapper `expansao` Sharepoint '''
    table = handler.get_element('EXPANSAO_RELATORIO', 'TOTAL')
    html = table.get_attribute('innerHTML')
    if html is None:
        raise ElementNotFoundException()
    return read_html(StringIO(html))[1]

def scrapper_manutencao(handler: WebHandler) -> DataFrame:
    ''' Function to scrapper `manutencao` Sharepoint '''
    return DataFrame() # TODO - Implement method

def sharepoint_scrapper() -> None:
    ''' Main function to handle sharepoints scrapper '''
    report_path = str(CONFIGS.get('ODLPATH', os.path.join(BASE_FOLDER, 'odl')))
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    with WebHandler('EXPANSAO_SHAREPOINT') as handler:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filepath = os.path.join(report_path, 'expansao_' + timestamp + '.csv')
        df = scrapper_expansao(handler)
        df.to_csv(filepath, index=False)
    with WebHandler('MANUTENCAO_SHAREPOINT') as handler:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filepath = os.path.join(report_path, 'manutencao_' + timestamp + '.csv')
        df = scrapper_manutencao(handler)
        df.to_csv(filepath, index=False)
