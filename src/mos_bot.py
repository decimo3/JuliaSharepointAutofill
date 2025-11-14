#!/bin/env python
''' Project to automate SharePoint form fill '''
from helpers.bannershow import print_header_presentation
from helpers.runchecker import instance_checker
from helpers.updater import update_chromedriver
from helpers.constants import CONFIGS
from helpers.dialogator import show_popup_error
from webhandler.scrapper import sharepoint_scrapper
from webhandler.formfill import SharePointFormFill

if __name__ == '__main__':
    print_header_presentation()
    instance_checker()
    update_chromedriver()
    mode = str(CONFIGS.get('OPERACAO', ''))
    if mode == 'EXTRAIR':
        sharepoint_scrapper()
    elif mode == 'INSERIR':
        filler = SharePointFormFill()
        filler.sharepoint_fillform()
    else:
        show_popup_error('O modo de operação é inválido!')
