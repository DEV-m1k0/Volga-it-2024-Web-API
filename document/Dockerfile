FROM python:3.11-alpine

WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt

CMD sleep 20 \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py add_roles \
    && python manage.py add_users \
    && echo "y" | python manage.py search_index --rebuild \
    && python manage.py runserver 0.0.0.0:8000

EXPOSE 8000