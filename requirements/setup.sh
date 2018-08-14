#!/usr/bin/env bash

# setup database
sudo -u postgres psql -c "CREATE USER cherry_user WITH ENCRYPTED PASSWORD 'tYSk4dqaW7Hq4cw2r4hP';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET CLIENT_ENCODING TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET TIMEZONE TO 'utc';"
sudo -u postgres psql -c "CREATE DATABASE cherry_db OWNER cherry_user;"
