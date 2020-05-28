#!/bin/bash

ACTION=$1
ORANGE='\033[0;33m'
NOCOLOR='\033[0m'

# Functions
show_menu() {
  clear
  echo -e "${ORANGE}
  --------------------
  BAOBAB SCRIPT MENU
  --------------------${NOCOLOR}"
  echo "
  Use one of the following command
  1) create_db    - Create database
  2) delete_db    - Delete database
  3) back_db      - Backup database
  4) restore_db   - Restore backed up database
  5) create_user  - Create user
  6) delete_user  - Delete user
  "
}

delete_db() {
  echo "Deleting database..."
  dropdb -U ${BAOBAB_USER} -i -e ${BAOBAB_DATABASE}
  echo "Deleting migrations folder.."
  rm -rf baobab-api/migrations
}

create_user() {
  echo "Creating user"
  createuser --interactive --pwprompt
}

delete_user() {
  echo "Deleting user..."
  dropuser ${BAOBAB_USER}
}

create_db() {
  echo "Creating database..."
  createdb -O ${BAOBAB_USER} ${BAOBAB_DATABASE}
}

back_db() {
  echo "Dumping database..."
  pg_dump ${BAOBAB_DATABASE}  > baobabdb_backup.sql
}

restore_db() {
  echo "Restoring database..."
  psql --set ON_ERROR_STOP=on ${BAOBAB_DATABASE} < baobabdb_backup.sql
}

case $ACTION in
    "create_db") create_db ;;
    "delete_db") delete_db ;;
    "create_user") create_user ;;
    "delete_user") delete_user ;;
    "back_db") back_db ;;
    "restore_db") restore_db ;;
    *) show_menu ;;
esac
