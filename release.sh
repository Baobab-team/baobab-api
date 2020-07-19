echo "Running upgrade ..."
python manage.py db upgrade

echo "Seeding data ..."
python manage.py seed_db
