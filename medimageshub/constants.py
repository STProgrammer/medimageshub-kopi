from .settings import DEBUG

HOST = ''
 
if DEBUG:
    HOST = 'http://127.0.0.1:8000'
else:
    HOST = 'https://medimageshub.azurewebsites.net'
