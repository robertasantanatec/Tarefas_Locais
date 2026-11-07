FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
RUN mkdir /app/data
VOLUME ["/app/data"]
ENTRYPOINT ["python", "-m", "src"]
CMD ["listar"]
