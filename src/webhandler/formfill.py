'''
Module to check recursively folders to fill sharepoint form

A função deve pecorrer a pasta `data` para procurar documentos e informações a
serem enviadas para o formulário do sharepoint. Os documentos estarão em duas
pastas diferentes de acordo com o serviço: manutencaoeconstrucao ou expansao.
Cada tipo de serviço atende a um formulário diferente mas as informações para
ambos os formulários estão na planilha `consulta_medicao_completa.xlsx`.
'''
import os
from helpers.constants import BASE_FOLDER, CONFIGS
from helpers.dialogator import show_popup_info, show_popup_error
from helpers.excelhandler import get_dataframe_from_excel
from .formfill_expansao import formfill_expansao
from .formfill_manutencao import formfill_manutencao

excel_path = os.path.join(BASE_FOLDER, 'consulta_medicao_completa.xlsx')
if not os.path.exists(excel_path):
    error_message = 'O relatório "consulta_medicao_completa.xlsx" não foi encontrado!'
    show_popup_error(error_message)
    raise FileNotFoundError(error_message)
DATAFRAME = get_dataframe_from_excel(excel_path)
MAX_DEPTH = int(str(CONFIGS.get('PROFUNDIDADE', '0')))

def fill_form(current_folder: str) -> None:
    ''' Function to separate projects by sector to be sent to the corresponding SharePoint '''
    expansao_projects: List[Tuple[List[str], DataFrame]] = []
    manutencao_projects: List[Tuple[List[str], DataFrame]] = []
    items = os.listdir(current_folder)
    for file_or_dir in items:
        orderid = file_or_dir.split('\\')[-1].replace('.pdf', '')
        try:
            medicao = int(orderid)
        except ValueError:
            medicao = None
        orderdt = (
            DATAFRAME[DATAFRAME['Num. da Medição'].isin([medicao]) | DATAFRAME['Origem'].isin([orderid])]
            if medicao is not None else
            DATAFRAME[DATAFRAME['Origem'].isin([orderid])]
        )
        if orderdt.empty:
            show_popup_info(f'O serviço {orderid} não foi encontrado na medição! Necessário inserir!')
            continue
        orderdt = orderdt.reset_index(drop=True)
        orderdt.index += 8
        filelist = (
            [file_or_dir]
            if not os.path.isdir(file_or_dir) else
            os.listdir(file_or_dir)
        )
        setor = orderdt['Setor'].iloc[0]
        if setor == 'Expansão':
            expansao_projects.append((filelist, orderdt))
        if setor in {'Manutenção', 'Qualidade'}:
            manutencao_projects.append((filelist, orderdt))
        show_popup_info(f'O setor "{setor}" do projeto {orderid} é inválido! O mesmo não será enviado!')
    # Enviando os arquivos...
    with WebHandler('EXPANSAO_SHAREPOINT') as handler:
        for filelist, orderdt in expansao_projects:
            formfill_expansao(handler, orderdt, filelist)
    with WebHandler('MANUTENCAO_SHAREPOINT') as handler:
        for filelist, orderdt in manutencao_projects:
            formfill_manutencao(handler, orderdt, filelist)

def recursive_search(current_folder: str, cur_depth: int) -> None:
    ''' Function to search recursivily to folders to find documents to send '''
    if cur_depth > MAX_DEPTH:
        return
    if cur_depth == MAX_DEPTH:
        fill_form(current_folder)
        return
    items = os.listdir(current_folder)
    for item in items:
        current_item = os.path.join(current_folder, item)
        if os.path.isdir(current_item):
            recursive_search(current_item, cur_depth + 1)

def sharepoint_fillform() -> None:
    ''' Main function to handle sharepoint form '''
    UPOFOLDER = str(CONFIGS.get('UPOPATH', ''))
    if not UPOFOLDER or not os.path.exists(UPOFOLDER):
        error_message = 'A pasta definida em "UPOPATH" não está acessível!'
        show_popup_error(error_message)
        raise ValueError(error_message)
    recursive_search(UPOFOLDER, 1)
