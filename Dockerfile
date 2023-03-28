FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=your_password
ENV DB_NAME=your_db_name

EXPOSE 8080

CMD ["python", "-u", "app.py"]
