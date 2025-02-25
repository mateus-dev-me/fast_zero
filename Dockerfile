FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR src/
COPY . .

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 app.main:api
