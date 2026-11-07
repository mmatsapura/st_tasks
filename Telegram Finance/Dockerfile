FROM python:3.14-alpine
LABEL authors="Acer"
ENV PYTHONUNBUFFERED=1
WORKDIR /Telegram-Finance
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]