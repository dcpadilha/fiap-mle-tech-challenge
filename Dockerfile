FROM public.ecr.aws/docker/library/python:3.11-slim-bullseye
ENV POETRY_VIRTUALENVS_CREATE=false

RUN mkdir -p ~/app/downloads

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 fiap-mle-tech-challenge.app:app
