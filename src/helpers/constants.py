''' Module to hold constants and configurations values '''
import os
import sys
from dotenv import dotenv_values

# Set what environment it is
DEV_ENV = not getattr(sys, 'frozen', False)

# Define App name by file name
APPNAME = (
    sys.argv[0].split('\\')[-1].replace('.exe','')
    if not DEV_ENV else
    sys.argv[0].split('\\')[-1].replace('.py','')
)

# Set variable that define the folder that it's executed
BASE_FOLDER = (
    os.path.dirname(sys.executable)
    if not DEV_ENV else
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Load configuration file
configuration_filepath = os.path.join(BASE_FOLDER, APPNAME + '.conf')
CONFIGS = dotenv_values(configuration_filepath)

# Load webelements path file
webelements_filepath = os.path.join(BASE_FOLDER, APPNAME + '.path')
WAYPATH = dotenv_values(webelements_filepath)
