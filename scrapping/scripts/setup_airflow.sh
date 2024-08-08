#!/bin/bash
mkdir -p ./temp/dags ./temp/logs ./temp/plugins
cp -R ./scrapping/airflow/dags ./temp
cp -R ./scrapping/utils.py ./temp/dags
docker compose up -d