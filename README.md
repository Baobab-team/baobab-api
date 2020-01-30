# Baobab


### Preriquisites
* [PostgreSQL](https://www.postgresql.org)



### Local setup 

```
# enter postgres
psql

# create database
CREATE DATABASE baobab_dev;

# Exit postgres
exit

# Setup environment variables for local development without docker
mv .env.local .env 

# Create database
python manage.py create_db

# Seed database
python manage.py seed_db 

# Launch app
python manage.py run

```


