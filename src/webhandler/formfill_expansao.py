''' Module to handle with fill `expansao` Sharepoint '''
import pandas
from helpers.constants import WAYPATH
from .webhandler import WebHandler

def formfill_expansao(infolist: pandas.DataFrame, filelist: list[str]) -> None:
    ''' Function to handle with fill `expansao` Sharepoint '''
    url = str(WAYPATH.get('EXPANSAO_SHAREPOINT', ''))
    firstline = infolist.iloc[0].to_dict()
    with WebHandler(url) as handler:
        handler.get_element('EXPANSAO_NEWITEM', 'TOTAL').click()
        print(handler.get_element('EXPANSAO_EMPREITEIRA', 'LONGA'))
        handler.get_element('EXPANSAO_PROJETO', 'INSTA').send_keys(firstline['Origem'])
        handler.get_element('EXPANSAO_MEDICAO', 'INSTA').send_keys(firstline['Num. da Medição'])
        handler.select_option(handler.get_element('EXPANSAO_CONTRATO', 'INSTA'), firstline['Contrato'])
        handler.select_option(handler.get_element('EXPANSAO_SETOR', 'INSTA'), firstline['Setor'])
        # handler.select_option(handler.get_element('EXPANSAO_ORIGEM', 'INSTA'), firstline['?'])
        handler.select_option(handler.get_element('EXPANSAO_BASE', 'INSTA'), firstline['Regional'])
        # handler.select_option(handler.get_element('EXPANSAO_STATUS', 'INSTA'), firstline['?'])
        handler.get_element('EXPANSAO_TRECHO', 'INSTA').send_keys(firstline['Trecho'])
        handler.get_element('EXPANSAO_EQUIPAMENTO', 'INSTA').send_keys(firstline['Equipamento'])
        handler.get_element('EXPANSAO_CIRCUITO', 'INSTA').send_keys(firstline['Circuito'])
        handler.get_element('EXPANSAO_SERVICO', 'INSTA').send_keys(firstline['Num Ocorrência'])
        # handler.get_element('EXPANSAO_RME', 'INSTA').send_keys(firstline['Num Ocorrência'])
        handler.get_element('EXPANSAO_ENDERECO', 'INSTA').send_keys(firstline['Endereço'])
        handler.get_element('EXPANSAO_MUNICIPIO', 'INSTA').send_keys(firstline['Município'])
        handler.get_element('EXPANSAO_INICIO', 'INSTA').send_keys(firstline['Início'])
        handler.get_element('EXPANSAO_FINAL', 'INSTA').send_keys(firstline['Término'])
        handler.get_element('EXPANSAO_SOLICITANTE', 'INSTA').send_keys(firstline['Téc Cliente'])
        handler.select_option(handler.get_element('EXPANSAO_RESPONSAVEL', 'INSTA'), firstline['Responsável Trabalho'])
        handler.get_element('EXPANSAO_DATAMEDICAO', 'INSTA').send_keys(firstline['Data Lançamento'])
        for i, row in infolist.iterrows():
            handler.get_element('EXPANSAO_ENCARREGADO', 'INSTA', i).send_keys(row['Encarregado'])
            handler.get_element('EXPANSAO_PONTOTRECHO', 'INSTA', i).send_keys(row['Observações'])
            handler.select_option(handler.get_element('EXPANSAO_ATIVIDADE', 'INSTA', i), row['atividade'])
            handler.get_element('EXPANSAO_CODIGOSAP', 'INSTA', i).send_keys(row['CodSAP'])
            handler.get_element('EXPANSAO_DESCRICAO', 'INSTA', i).send_keys(row['DescServiço'])
            # handler.get_element('EXPANSAO_UNIDADE', 'INSTA', i).send_keys(row['?'])
            handler.get_element('EXPANSAO_QUANTIDADE', 'INSTA', i).send_keys(row['Qde Exec'])
            handler.get_element('EXPANSAO_VALORUND', 'INSTA', i).send_keys(row['ValorUnit'])
            handler.get_element('EXPANSAO_VALOREXEC', 'INSTA', i).send_keys(row['ValorTotal'])
            handler.select_option(handler.get_element('EXPANSAO_MESPGMT', 'INSTA', i), row['MesPagto'])
        handler.get_element('EXPANSAO_FILEBTN', 'MEDIA').click()
        handler.get_element('EXPANSAO_FILEFORM', 'INSTA').send_keys('\n'.join(filelist))
        handler.get_element('EXPANSAO_FILESEND', 'MEDIA').click()
        handler.get_element('EXPANSAO_SENDFORM', 'MEDIA').click()
