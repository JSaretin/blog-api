from deta import Deta 
from os import environ

if environ.get('DEBUG'):
    deta = Deta(environ['DETA_API_KEY'])
else:
    deta = Deta()

def get_connection(db_name: str):
    return deta.Base(f'blog_{db_name}')

def get_drive():
    return deta.Drive('blog')