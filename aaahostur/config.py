import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    # CONFIG FOR CUSTOM OAUTH SERVER
    SECRECT_KEY = os.getenv('FLASK_SECRET_KEY')

    SESSION_TYPE = os.getenv('SESSION_TYPE')
     
    # CONFIG FOR MYSQL
    DEBUG = os.getenv('DEBUG')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')


# dicicionario apuntando a la clase para coger la informacion de ella  
config = {
        'development': Config
   } 