FROM python:3.10

WORKDIR /code

COPY requirements.txt requirements.txt
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./compile_levi_model.py"]
