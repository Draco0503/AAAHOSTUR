# AAAHOSTUR
 Trabajo de Fin de Ciclo DAM
> *Realizado por [Despinosa](https://github.com/Despinosa), [Draco0503](https://github.com/Draco0503) y [Tecnodwarff](https://github.com/Tecnodwarff)*
---
## Requisitos previos

---
* **Python** 3.10
* pip 23.1.2 (también vale *latests*)
* Acceso a base de datos en **MySQL** como administrador


## Instalación

---
Lo primero de todo necesitamos instalar las dependencias, para ello podemos ejecutar el comando:

Windows

```commandline
pip install python-dotenv passlib mysqlclient Flask SQLAlchemy flask-sqlalchemy SQLAlchemy-Utils bcrypt PyJWT user_agents uuid
```

Linux (puede que tengas *pip3*, si es así, el comando es el mismo pero con *pip3*)

```commandline
sudo apt install libmysqlclient-dev

pip install python-dotenv passlib Flask SQLAlchemy flask-sqlalchemy SQLAlchemy-Utils bcrypt PyJWT user_agents uuid
```

Por si estas líneas no funcionan dejamos las librerías con sus respectivas versiones:

```text
python-dotenv==0.21.0
mysqlclient==2.1.1  # Esta no en Linux
Flask==2.2.2
SQLAlchemy==2.0.13
flask-sqlalchemy==3.0.2
SQLAlchemy-Utils==0.38.3
bcrypt==4.0.1
PyJWT==2.7.0
user_agents==2.2.0
uuid==1.30
```

> **NOTA:** Estas librerías debería de descargar automáticamente sus sub-dependecias

Al usar SQLAlchemy, un ORM de Python con compatibilidad con Flask, no es necesario ejecutar los scripts de la base de datos pero **SI MUY RECOMENDABLE**, aun así está preparado para ser ejecutado directamente con los scripts:


* **createDBTables.bat**, para Windows
* **createDBTables.sh**, para Linux

Su uso es:

```commandline
createDBTables nombre_base_datos usuario contraseña
```

Este script te tira la base de datos, si ya existía, y te la crea llegando a insertar los datos necesarios para el funcionamiento del programa.

Por último y no menos importante, necesitas crear un archivo llamado ".env" dentro de la carpeta de "aaahostur", el cual amacenará las claves necesarias para el funcionamiento del programa, como la conexión a la base de datos y la firma y algoritmo de cifrado de los JWTs

Ese archivo a de contener:

```text
# JWT TOKEN REQUIREMENTS
# JWT SECRET SIGN
FLASK_SECRET_KEY=
# RECOMMENDED HS256
ALGORITHM=

# SOME DEBUG PARAMS
# null or filesystem
SESSION_TYPE=filesystem
DEBUG=True

## MYSQL SERVER KEYS
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=
```

## Despliegue

---
Una vez preparado el entorno podemos desplegar la aplicación. Para ello nos situamos en la carpeta principal "AAAHOSTUR" y ejecutamos:
(Ejecutarlo como "sudo" para Linux)

```commandline
python ./aaahostur/app.py
```

