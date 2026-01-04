"""
ASGI config for shahin_auto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
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

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shahin_auto.settings')

application = get_asgi_application()