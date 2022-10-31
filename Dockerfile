# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

EXPOSE 80

WORKDIR /app

# make sure that wget is installed
RUN apt-get update && apt-get install -y wget

# ensure that pdf2txt.py is installed using pip install pdfminer.six and flask
RUN pip install pdfminer.six flask openai 

COPY . .

# run the file server.py with python3
CMD ["python3", "server.py"]
