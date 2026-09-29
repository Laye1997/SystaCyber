FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Code de l'application
COPY . .

# Collecte des fichiers statiques (clé factice : sert uniquement au build)
RUN SECRET_KEY=build-only DEBUG=false DJANGO_SETTINGS_MODULE=config.settings \
    python manage.py collectstatic --noinput

# La plateforme fournit $PORT ; on l'écoute et on migre au démarrage.
EXPOSE 8000
CMD sh -c "python manage.py migrate --noinput && gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 3 --log-file -"
