#!/bin/bash

# Name of virtual environment to create
ENVNAME=cherrynote

# Prepare requirements
sudo apt update

# Python
sudo apt install python3 python3-pip python3-dev -y

# PostgreSQl
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt update
sudo apt install libxslt-dev libxml2-dev libpam-dev libedit-dev -y
sudo apt install postgresql postgresql-contrib postgresql-server-dev-10 -y
# Generating and setting locale settings
sudo locale-gen en_US.UTF-8
sudo localedef -i en_US -f UTF-8 en_US.UTF-8
# Setting up database
sudo -u postgres psql -c "CREATE USER cherry_user WITH ENCRYPTED PASSWORD 'tYSk4dqaW7Hq4cw2r4hP';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET CLIENT_ENCODING TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE cherry_user SET TIMEZONE TO 'utc';"
sudo -u postgres psql -c "CREATE DATABASE cherry_db OWNER cherry_user;"

# Installing virtualenvwrapper
pip3 install virtualenvwrapper
# Setting up virtualenv wrapper
echo "export WORKON_HOME=$HOME/.virtualenvs
source $(sudo find /usr -name virtualenvwrapper.sh)" >> ~/.bashrc
source ~/.bashrc
# Creating `cherrynote` virtual environment
mkvirtualenv $ENVNAME --python=$(which python3)
# Activating virtual environment
workon $ENVNAME

# Installing Python requirements
pip install -r requirements/local.txt

# Preparing application env data
mv .env.example .env
# Creating database scheme
./manage.py migrate
# Creating super user account
./manage.py createsuperuser