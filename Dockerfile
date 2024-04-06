from python : 3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirments.txt / app / 

RUN pip3 install --upgrade pip
RUN pip3 install -r requirments.txt


COPY ./core/app

CMD ["python3","mange.py","runserver","0.0.0.0:8000"]