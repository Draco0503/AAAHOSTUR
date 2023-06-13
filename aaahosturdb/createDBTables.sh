#!/bin/bash
user=$2
passwd=$3
db=$1

if [ "$db" = "" ]; then
    echo "Uso: $0 host db_name user password"
    exit 1
fi

sudo mysql --user=$user --password=$passwd -e "drop database if exists $db; create database $db"

for sql_file in ./tables/*.sql; do
    echo "Importing $sql_file";
    sudo mysql --user=$user --password=$passwd $db < $sql_file;
done