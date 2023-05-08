@echo off

SET user=%2
SET passwd=%3
SET db=%1

echo "Paso 0 completado"

IF [%db%]==[]  (
    echo "Uso: %0 db user pwd"
    exit -1
) 

echo "Paso 1, primera comprobacion"

mysql --user=%user% --password=%passwd% -e "drop database if exists %db%; create database %db%"

echo "Paso 2 completado"

for %%f in (.\tables\*) do (
    echo "Importing file: %%f"
    mysql --user=%user% --password=%passwd% %db% < %%f
)