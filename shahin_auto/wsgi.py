"""
WSGI config for shahin_auto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

# PyMySQL compatibility shim - must be before Django imports
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    # Set version to satisfy Django's version check
    import MySQLdb
    MySQLdb.version_info = (2, 2, 7, 'final', 0)
    MySQLdb.__version__ = '2.2.7'
except (ImportError, AttributeError):
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shahin_auto.settings')

application = get_wsgi_application()