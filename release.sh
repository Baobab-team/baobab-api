python manage.py db upgrade

if [ "$APP_SETTINGS" == "app.config.StagingConfig" ]
then
  echo "Environment: Staging"
  echo "Seeding data ..."
  python manage.py seed_db
fi
