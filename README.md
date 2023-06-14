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
pip install -r requirements.txt
```

Linux (puede que tengas *pip3*, si es así, el comando es el mismo pero con *pip3*)

```commandline
sudo apt install libmysqlclient-dev

pip install -r requirements.txt
```

Por si estas líneas no funcionan dejamos las librerías con sus respectivas versiones:

```text
bcrypt==4.0.1
certifi==2023.5.7
charset-normalizer==3.1.0
click==8.1.3
colorama==0.4.6
Flask==2.2.2
Flask-SQLAlchemy==3.0.2
greenlet==2.0.2
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
mysqlclient==2.1.1
passlib==1.7.4
PyJWT==2.7.0
python-dotenv==0.21.0
requests==2.31.0
SQLAlchemy==2.0.13
SQLAlchemy-Utils==0.38.3
typing_extensions==4.6.3
ua-parser==0.16.1
urllib3==2.0.3
user-agents==2.2.0
uuid==1.30
Werkzeug==2.3.6
```

> **NOTA:** Estas librerías debería de descargar automáticamente sus sub-dependecias

**LA BASE DE DATOS TIENE QUE ESTAR CREADA PARA QUE FUNCIONE EL ORM**
```commandline
CREATE DATABASE nombre_base_datos
```

Al usar SQLAlchemy, un ORM de Python con compatibilidad con Flask, no es necesario ejecutar los scripts de la base de datos pero **SI MUY RECOMENDABLE**, aun así está preparado para ser ejecutado directamente con los scripts:


* **createDBTables.bat**, para Windows
* **createDBTables.sh**, para Linux

Su uso es:

```commandline
createDBTables nombre_base_datos usuario contraseña
```

Este script te tira la base de datos, si ya existía, y te la crea llegando a insertar los datos necesarios para el funcionamiento del programa.

Si has optado por el ORM, una vez cargada las tablas de la base de datos necesitamos los datos iniciales, éstos están en [aaahosturdb/tables](/aaahosturdb/tables), en el archivo **50_InsertsIniciales.sql**.

Para cargarlos puedes hacerlo desde un Workbench (**RECOMENDABLE**, ya que pilla el encoding para las tildes) o desde línea de comandos una vez registrado desde la terminal de mysql:
```commandline
mysql -u tu_usuario -p
Enter password: **************

mysql> use nombre_de_tu_base_de_datos;
mysql> source C:/ruta/hasta/el/proyecto/AAAHOSTUR/aaahosturdb/50_InsertsIniciales.sql;
```


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

