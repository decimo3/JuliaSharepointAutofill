''' Module to handle with fill `expansao` Sharepoint '''
import pandas
from helpers.constants import WAYPATH
from helpers.dialogator import show_popup_debug
from .webhandler import WebHandler

def formfill_expansao(infolist: pandas.DataFrame, filelist: list[str]) -> None:
    ''' Function to handle with fill `expansao` Sharepoint '''
    url = str(WAYPATH.get('EXPANSAO_SHAREPOINT', ''))
    firstline = infolist.iloc[0].to_dict()
    with WebHandler(url) as handler:
        handler.get_element('EXPANSAO_NEWITEM', 'TOTAL').click()
        if handler.get_elements('EXPANSAO_DIALOGBTN', 'TOTAL'):
            handler.get_element('EXPANSAO_DIALOGBTN', 'AGORA').click()
        # handler.get_element('EXPANSAO_EMPREITEIRA', 'LONGA')
        handler.get_element('EXPANSAO_PROJETO', 'AGORA', None, None, firstline['Origem'])
        handler.get_element('EXPANSAO_MEDICAO', 'AGORA', None, None, firstline['Num. da Medição'])
        handler.select_option('EXPANSAO_CONTRATO', 'AGORA', None, None, firstline['Contrato'])
        handler.select_option('EXPANSAO_SETOR', 'AGORA', None, None, firstline['Setor'])
        # handler.select_option(handler.get_element('EXPANSAO_ORIGEM', 'AGORA', None, None, firstline['?'])
        handler.select_option('EXPANSAO_BASE', 'AGORA', None, None, firstline['Regional'])
        # handler.select_option(handler.get_element('EXPANSAO_STATUS', 'AGORA', None, None, firstline['?'])
        handler.get_element('EXPANSAO_TRECHO', 'AGORA', None, None, firstline['Trecho'])
        handler.get_element('EXPANSAO_EQUIPAMENTO', 'AGORA', None, None, firstline['Equipamento'])
        handler.get_element('EXPANSAO_CIRCUITO', 'AGORA', None, None, firstline['Circuito'])
        handler.get_element('EXPANSAO_SERVICO', 'AGORA', None, None, firstline['Num Ocorrência'])
        # handler.get_element('EXPANSAO_RME', 'AGORA', None, None, firstline['Num Ocorrência'])
        handler.get_element('EXPANSAO_ENDERECO', 'AGORA', None, None, firstline['Endereço'])
        handler.get_element('EXPANSAO_MUNICIPIO', 'AGORA', None, None, firstline['Município'])
        handler.get_element('EXPANSAO_INICIO', 'AGORA', None, None, firstline['Início'])
        handler.get_element('EXPANSAO_FINAL', 'AGORA', None, None, firstline['Término'])
        handler.select_option('EXPANSAO_SOLICITANTE', 'AGORA', None, None, 'WELITON BARBOSA CHAGAS') # FIXME - firstline['Téc Cliente']
        handler.get_element('EXPANSAO_RESPONSAVEL', 'AGORA', None, None, firstline['Responsável Trabalho'])
        handler.get_element('EXPANSAO_DATAMEDICAO', 'AGORA', None, None, firstline['Data Lançamento'])
        for i, row in infolist.iterrows():
            handler.get_element('EXPANSAO_ENCARREGADO', 'AGORA', i, None, row['Encarregado'])
            handler.get_element('EXPANSAO_PONTOTRECHO', 'AGORA', i, None, row['Observações'])
            handler.select_option('EXPANSAO_ATIVIDADE', 'AGORA', i, None, row['atividade'])
            if handler.get_elements('EXPANSAO_CODIGOSAP1', 'AGORA', i, None):
                handler.get_element('EXPANSAO_CODIGOSAP1', 'AGORA', i, None, row['CodSAP'])
            else:
                handler.get_element('EXPANSAO_CODIGOSAP2', 'AGORA', i, None, row['CodSAP'])
            handler.get_element('EXPANSAO_DESCRICAO', 'AGORA', i, None, row['DescServiço'])
            # handler.get_element('EXPANSAO_UNIDADE', 'AGORA', i, None, row['?'])
            handler.get_element('EXPANSAO_QUANTIDADE', 'AGORA', i, None, row['Qde Exec'])
            handler.get_element('EXPANSAO_VALORUND', 'AGORA', i, None, row['ValorUnit'])
            handler.get_element('EXPANSAO_VALOREXEC', 'AGORA', i, None, row['ValorTotal'])
            handler.select_option('EXPANSAO_MESPGMT', 'AGORA', i, None, row['MesPagto'][:3])
        handler.get_element('EXPANSAO_FILEBTN', 'MEDIA').click()
        handler.get_element('EXPANSAO_FILEFORM', 'AGORA', None, None, '\n'.join(filelist))
        handler.get_element('EXPANSAO_FILESEND', 'MEDIA').click()
        handler.get_element('EXPANSAO_SENDFORM', 'MEDIA').click()
        show_popup_debug(f'Medição {firstline['Num. da Medição']} enviado com sucesso!')
