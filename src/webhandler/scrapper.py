''' Module to scrapper Sharepoint forms '''
from io import StringIO
from datetime import datetime
from pandas import DataFrame, read_html
from webhandler.webhandler import WebHandler, ElementNotFoundException

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
    with WebHandler('EXPANSAO_SHAREPOINT') as handler:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        df = scrapper_expansao(handler)
        df.to_csv(f'expansao_{timestamp}.csv', index=False)
    with WebHandler('MANUTENCAO_SHAREPOINT') as handler:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        df = scrapper_manutencao(handler)
        df.to_csv(f'manutencao_{timestamp}.csv', index=False)
