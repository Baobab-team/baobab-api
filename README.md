# Baobab


``cd baobab``

#### Create virtual environment 
```

virtualenv env #or another tool
source env/bin/active

```

#### Install the dependencies
```
pip install -r requirements

```

#### Setup .env
```
touch .env
APP_SETTINGS="config.DevelopmentConfig" >> .env
FLASK_ENV=development >> .env
SECRET_KEY= <<< DEMANDE LA CLE >>>
```


#### Postgres DB
1. [Install PostgreSQL](https://www.postgresql.org)
2. Create a local database 
3. Add the url to .env
 ```
 DATABASE_URL="postgresql://localhost/DB_NAME" >> .env  
 ```

