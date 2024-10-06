FROM python:3.11-alpine

WORKDIR /app
ADD . /app/

RUN pip install -r requirements.txt

CMD sleep 15 && python manage.py runserver 0.0.0.0:8000
    
EXPOSE 8000