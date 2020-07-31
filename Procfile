release: ./release.sh
web: gunicorn "app:create_app()"
DATABASE_URL=$(heroku config:get DATABASE_URL -app baobab-migrations-staging) web
