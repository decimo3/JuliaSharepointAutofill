#!/bin/env python
''' Project to automate SharePoint form fill '''
from helpers.bannershow import print_header_presentation
from helpers.runchecker import instance_checker
from helpers.updater import update_chromedriver

if __name__ == '__main__':
    print_header_presentation()
    instance_checker()
    update_chromedriver()
    # TODO - Check fillorders
    # TODO - Startup webhandler
    # TODO - Fill workorders
