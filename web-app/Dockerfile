FROM python:3.10-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install --no-cache-dir pipenv

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE 5000

CMD ["pipenv", "run", "python", "app.py"]