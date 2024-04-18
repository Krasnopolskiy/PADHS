#!/bin/bash

echo "Apply database migrations"
alembic upgrade head

exec "$@"
