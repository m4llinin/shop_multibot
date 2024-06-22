# Используем базовый образ Python
FROM python:3.11

# Установка зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копирование исходного кода
COPY . /app

# Установка рабочей директории
WORKDIR /app

# Запуск бота
CMD ["python", "app.py"]