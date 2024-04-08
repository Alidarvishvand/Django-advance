FROM python:3.11.4-slim-buster

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirments.txt /app/ 

RUN pip3 install --upgrade pip
RUN pip3 install -r requirments.txt


COPY ./core /app

# CMD ["python3","manage.py","runserver","0.0.0.0:8000"]