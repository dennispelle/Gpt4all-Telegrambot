FROM python:3.9

WORKDIR /app

COPY /Bot/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "bot.py"]
