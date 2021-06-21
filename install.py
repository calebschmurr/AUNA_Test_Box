#Install.py - installation script.

import sys
import subprocess


#Install wxPython
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-U', 'wxPython'])

#install PIL
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])

#Install serial
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyserial'])
