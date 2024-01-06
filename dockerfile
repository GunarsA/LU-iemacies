FROM python:3.12

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind build

RUN python manage.py migrate
RUN python manage.py loaddata fixtures.json

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]