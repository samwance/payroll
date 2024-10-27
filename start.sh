#!/usr/bin/env bash
# -*- coding: utf-8 -*-
export ENVIRONMENT=local
export PYTHONDONTWRITEBYTECODE=1
template_env=.env.template
main_env=src/.env

if [[ ! -e ${main_env} ]]
then
    cp "${template_env}"  "${main_env}"
    sed 's|payroll-db|127.0.0.1|g'  ${template_env}
fi

docker compose -f docker/docker-compose.yml up -d --build
poetry run alembic -c src/alembic.ini upgrade head && alembic -c src/alembic.ini stamp head && python src/main.py &

cd frontend/vue-app
npm install
npm run serve

docker compose -f docker/docker-compose.yml down
exit
