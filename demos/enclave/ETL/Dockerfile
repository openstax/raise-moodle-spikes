FROM python:3.10

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./compile_models.py"]