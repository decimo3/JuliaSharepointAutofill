''' Module to hold constants and configurations values '''
import os
import sys
from dotenv import load_dotenv

# Define App name by file name
APPNAME = sys.argv[0].split('\\')[-1]

# Set what environment it is
DEV_ENV = not getattr(sys, 'frozen', False)

# Set variable that define the folder that it's executed
BASE_FOLDER = (
    os.path.dirname(sys.executable)
    if not DEV_ENV
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Load configuration file
configuration_filepath = os.path.join(BASE_FOLDER, APPNAME + '.conf')
load_dotenv(configuration_filepath)
