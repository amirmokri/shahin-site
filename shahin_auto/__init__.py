# PyMySQL compatibility shim for Django
# This must be imported before Django loads the database backend
# This allows Django to use PyMySQL instead of mysqlclient
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    # Set version to satisfy Django's version check
    import MySQLdb
    MySQLdb.version_info = (2, 2, 7, 'final', 0)
    MySQLdb.__version__ = '2.2.7'
except (ImportError, AttributeError):
    pass

