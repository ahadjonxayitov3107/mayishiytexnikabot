# PythonAnywhere'da "Web" bo'limida WSGI configuration file ochiladi
# (odatda /var/www/SIZNING_USERNAME_pythonanywhere_com_wsgi.py manzilida).
# O'sha faylning ICHIDAGI HAMMA narsani o'chirib, o'rniga QUYIDAGINI joylashtiring
# (yo'llarni o'zingizning papka nomingizga moslang):

import sys

# Loyiha joylashgan papka yo'li (odatda /home/SIZNING_USERNAME/mayishiy-bot-py)
path = '/home/SIZNING_USERNAME/mayishiy-bot-py'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application  # noqa
