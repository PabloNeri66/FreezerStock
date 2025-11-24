#!/bin/bash
# Define a variável de ambiente do Django
export DJANGO_SETTINGS_MODULE=core.settings

# Roda o Uvicorn apontando para seu ASGI
uvicorn core.asgi:application --host 0.0.0.0 --port $PORT
