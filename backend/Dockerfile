FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pymongo

COPY ./backend /app

ENV FLASK_APP=server.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
