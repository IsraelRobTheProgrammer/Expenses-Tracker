#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python expensetracker/manage.py collectstatic --no-input

python expensetracker/manage.py migrate
