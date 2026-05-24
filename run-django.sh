#!/bin/bash

exec python3 manage.py migrate & \
exec gunicorn backend.wsgi