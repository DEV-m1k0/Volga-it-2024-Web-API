FROM python:3.11-alpine

WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt

CMD sleep 5 \
    && python manage.py makemigrations \ 
    && python manage.py migrate \
    && python manage.py add_roles \
    && python manage.py add_users \
    && python manage.py runserver 0.0.0.0:8000
    
EXPOSE 8000