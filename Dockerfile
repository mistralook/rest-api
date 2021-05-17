FROM python:3.8

RUN mkdir -p /app
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 8080
RUN chmod +x main.py
CMD ["python", "main.py"]