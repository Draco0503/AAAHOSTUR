import os
class Config():
    # CONFIG FOR CUSTOM OAUTH SERVER
    #app.secret_key = os.getenv('FLASK_SECRET_KEY')

    #SESSION_TYPE = os.getenv('SESSION_TYPE')
     
    # CONFIG FOR MYSQL

    #CON ESTO NO PILLA EL DEBUG
    #DEBUG = os.getenv('DEBUG')
    DEBUG = True
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')




# dicicionario apuntando a la clase para coger la informacion de ella  
config = {
        'development': Config
   } 