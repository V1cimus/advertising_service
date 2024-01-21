FROM python:3.11-slim
RUN apt-get update 
WORKDIR /src
RUN pip3 install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./src /src
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
