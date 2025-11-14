''' Module to scrapper Sharepoint forms '''
from io import StringIO
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
        df = scrapper_expansao(handler)
        df.to_csv('expansao.csv', index=False)
    with WebHandler('MANUTENCAO_SHAREPOINT') as handler:
        df = scrapper_manutencao(handler)
        df.to_csv('manutencao.csv', index=False)
