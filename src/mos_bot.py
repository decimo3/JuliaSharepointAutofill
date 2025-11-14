#!/bin/env python
''' Project to automate SharePoint form fill '''
from helpers.bannershow import print_header_presentation
from helpers.runchecker import instance_checker
from helpers.updater import update_chromedriver
from webhandler.scrapper import sharepoint_scrapper
from webhandler.formfill import SharePointFormFill

if __name__ == '__main__':
    print_header_presentation()
    instance_checker()
    update_chromedriver()
    sharepoint_scrapper()
    filler = SharePointFormFill()
    filler.sharepoint_fillform()
