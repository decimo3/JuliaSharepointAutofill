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
    headers = handler.get_elements('EXPANSAO_CABECALHOS', 'AGORA')
    if headers is None:
        raise ElementNotFoundException()
    head: list[str] = [col.text.strip() for col in headers]
    # Collect bodies
    lines = handler.get_elements('EXPANSAO_VALORACOES', 'AGORA')
    if lines is None:
        raise ElementNotFoundException()
    body: list[list[str]] = []
    for row in lines:
        cols: list[str] = [col.text.strip() for col in row.find_elements(By.XPATH, './td')]
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
