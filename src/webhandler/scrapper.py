''' Module to scrapper Sharepoint forms '''
from time import sleep
from pandas import DataFrame
from selenium.webdriver.common.by import By
from webhandler.webhandler import WebHandler, ElementNotFoundException

def scrapper_expansao(handler: WebHandler) -> DataFrame:
    ''' Function to scrapper `expansao` Sharepoint '''
    handler.get_element('EXPANSAO_RELATORIO', 'TOTAL')
    sleep(5)
    # Collect header
    head: list[str] = []
    headers = handler.get_elements('EXPANSAO_CABECALHOS', 'AGORA')
    if headers is None:
        raise ElementNotFoundException()
    head = [col.text.strip() if col.text.strip() else f'Coluna{i}' for i, col in enumerate(headers)]
    # Collect bodies
    body: list[list[str]] = []
    line_number = len(handler.get_elements('EXPANSAO_VALORACOES_LN', 'AGORA') or [])
    for i in range(line_number):
        cols: list[str] = []
        for j in range(len(head)):
            cols.append(handler.get_element('EXPANSAO_VALORACOES_XY', 'AGORA', i + 1, j + 1).text.strip())
        body.append(cols)
    return DataFrame(data=body, columns=head)

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
