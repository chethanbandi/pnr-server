activate_this = "/var/www/apps.sairahul.com/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/apps.sairahul.com/pnr")
from views import app as application

