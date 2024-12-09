FROM python:3.9-slim

   WORKDIR /app

   # Копируем файл с зависимостями
   COPY requirements.txt .

   # Устанавливаем зависимости
   RUN pip install --no-cache-dir -r requirements.txt

   # Копируем остальные файлы
   COPY . .

   CMD ["python", "тгпремселбот.py"]
