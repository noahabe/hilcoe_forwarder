FROM python:3.10 

WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY main.py /code/main.py

COPY config.json /code/config.json

CMD ["python", "main.py"]