echo "Running upgrade ..."
python manage.py db upgrade

echo "Environment: Staging"
echo "Seeding data ..."
python manage.py seed_db
