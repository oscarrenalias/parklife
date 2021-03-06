#
# set up the import path
#
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
sys.path.append(os.path.join(os.path.dirname(__file__), 'view'))                
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'instagram'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'google'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'google/atom'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'json'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'json/simplejson'))

# Must set this env var before importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'