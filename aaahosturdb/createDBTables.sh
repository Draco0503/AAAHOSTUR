#!/bin/bash
host=$1
user=$3
passwd=$4
db=$2
echo "Paso 0 completado"

if [ "$db" = "" ]; then
    echo "Uso: $0 host db_name user password"
    exit 1
fi

echo "Paso 1, primera comprobacion"

mysql --host=$host --user=$user --password=$passwd -e "drop database if exists $db; create database $db"

echo "Paso 2 completado"

for sql_file in ./tables/*.sql; do
    echo "Importing $sql_file";
    mysql --host=$host --user=$user --password=$passwd $db< $sql_file;
done