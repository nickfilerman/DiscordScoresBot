FROM python:3.11-bookworm
RUN pip3 install beautifulsoup4 requests discord

ADD . .

CMD ["python3", "./main.py"]