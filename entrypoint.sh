#!/usr/bin/env bash
set -euo pipefail

RETRIES=10


until flask --app "myapp" db upgrade >/dev/null 2>&1 || [ "$RETRIES" -le 0 ]; do
  echo "DB not ready yet, retrying... (${RETRIES} left)"
  RETRIES=$((RETRIES - 1))
  sleep 1
done

if [ "$RETRIES" -le 0 ]; then
  echo "Migrations still failing after retries. Exiting."
  exit 1
fi

echo "Running migrations"
flask --app myapp db upgrade

if [ "${RUN_SEED:-0}" = "1" ]; then
  echo "Seeding test data"
  flask --app myapp seed-testdata
fi

echo "Starting Flask built-in server"
exec flask --app myapp run --host=0.0.0.0 --port="${PORT:-8000}" --no-reload --no-debugger
