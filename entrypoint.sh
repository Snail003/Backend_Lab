#!/bin/sh
set -e


until pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}"; do
  echo "waiting for postgres..."
  sleep 1
done


if [ -d migrations ]; then
  flask --app myapp db upgrade
else
  flask --app myapp db init
  flask --app myapp db migrate -m "initial"
  flask --app myapp db upgrade
fi


flask --app myapp seed-testdata || true


flask --app myapp run --host=0.0.0.0 --port=8000