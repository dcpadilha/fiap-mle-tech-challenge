<<<<<<< HEAD
FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 2mlet_phase1.app:app
=======
FROM apache/airflow:2.5.1

COPY ./requirements.txt .

RUN pip install --no-cache --user -r requirements.txt
>>>>>>> gabriel
