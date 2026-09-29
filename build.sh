#!/usr/bin/env bash
# Script de build pour l'hébergeur (Render, etc.)
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
