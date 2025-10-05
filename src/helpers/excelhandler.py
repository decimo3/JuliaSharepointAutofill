''' Module to get dataframe from Excel file '''
import os
import pandas
import openpyxl
from .dialogator import show_popup_error, show_popup_debug

class WorksheetNotFoundException(Exception):
    ''' Exception to inform that worksheet was not found '''

def get_dataframe_from_excel(file_path: str) -> pandas.DataFrame:
    ''' Function to get DataFrame from Excel file '''
    if not os.path.exists(file_path):
        error_message = f'A arquivo {file_path} não está acessível!'
        show_popup_error(error_message)
        raise FileNotFoundError(error_message)
    show_popup_debug(f'Obtendo informações do arquivo {file_path}...')
    workbook = openpyxl.open(file_path)
    worksheet = workbook.active
    if not worksheet:
        error_message = 'A planilha ativa não pode ser definida!'
        show_popup_error(error_message)
        raise WorksheetNotFoundException(error_message)
    rows = worksheet.iter_rows(values_only=True)
    head = next(rows)
    body = list(rows)
    dataframe = pandas.DataFrame(body, columns=head)
    show_popup_debug('Planilha carregada em memória com sucesso!')
    return dataframe
