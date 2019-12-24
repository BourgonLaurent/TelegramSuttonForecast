FROM python:3

ADD run_bot.py /

RUN pip install python-telegram-bot bs4 Pillow suttonforecast-bourgonlaurent

CMD ["python", "./run_bot.py"]