FROM python:3.10.5

# bytecode are compiled versions of Python code are to speed up loading time but not necessary in containers
ENV PYTHONDONTWRITEBYTECODE=1

# disable buffering of stdout and stderr (will not cause delays in console output), reduces container size
#ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install pipenv
COPY ./Pipfile* ./

# exact versionns and system-wide (not in venv, will reduce the size of the container)
RUN pipenv install --deploy --system

COPY . .
RUN chmod +x wait-for-it.sh entrypoint.sh
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

ENTRYPOINT ["/code/entrypoint.sh"]
