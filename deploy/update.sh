#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/usr/local/apps/gender-classification'

cd $PROJECT_BASE_PATH
git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart gender-classification

echo "DONE! :)"
