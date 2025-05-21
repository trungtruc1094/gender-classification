#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/trungtruc1094/gender-classification.git'

PROJECT_BASE_PATH='/usr/local/apps/gender-classification'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

python3 -m venv $PROJECT_BASE_PATH/env

$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt uwsgi==2.0.21

# Run migrations
$PROJECT_BASE_PATH/env/bin/python $PROJECT_BASE_PATH/manage.py migrate

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/deploy/supervisor_gender-classification.conf /etc/supervisor/conf.d/gender-classification.conf
supervisorctl reread
supervisorctl update
supervisorctl restart gender-classification

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/deploy/nginx_gender-classification.conf /etc/nginx/sites-available/gender-classification.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/gender-classification.conf /etc/nginx/sites-enabled/gender-classification.conf
systemctl restart nginx.service

echo "DONE! :)"
