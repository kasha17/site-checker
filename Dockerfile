FROM python:3.8
COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code
WORKDIR /code
EXPOSE 8000
CMD ["python", "pup/manage.py", "runserver", "0.0.0.0:8000"]
