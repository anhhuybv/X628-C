# Install and using x628-c on linux
## Install environment
    NOTE:
    App to deployment and running on docker ( environment linux )
    
    ** Install python 2.7 **
    apt-get update
    apt-get upgrade
    apt-get install python
    apt-get install sudo
    apt-get install git
    
    ** Install flask **
    apt-get install python-pip
    apt-get install python3-pip
    pip install flask          
    pip install wtforms
    pip install psycopg2
    pip install psycopg2-binary

    ** Install postgresql **
    apt-get install postgresql
    sudo service postgresql restart
    sudo -i -u postgres
    sudo -u postgres psql postgres
    \password
    
    ** Create table for database **
    create table datatable (
    numerical serial primary key not null,
    iduser int not null,
    name text not null,
    date date not null,
    time time not null,
    method_swipe int not null);
    
    create table usertable (
    uid int primary key not null,
    iduser int not null,
    name text not null, 
    privilege text,
    password text,
    groupid text);
    
    create table timetable (
    numerical serial primary key not null,
    iduser int not null,
    name text not null,
    date date,
    timein time,
    timeout time,
    timelate time,
    timeearly time);
    
    
## Running
    git clone https://github.com/anhhuybv/X628-C.git
    cd X628-C
    ./run.sh
    (username: admin, password: techmaster)

## SDK python x628-c
    https://github.com/AlSayedGamal/python_zklib

## Command docker
    docker run --name db-x628-c -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres:9.6
    docker exec -it x628-c /bin/bash
    docker exec -it -u postgres db-x628-c psql