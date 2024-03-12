FROM python:3.11-bookworm

ADD . .

RUN pip3 install beautifulsoup4 requests discord

CMD ["python3", "./main.py"]