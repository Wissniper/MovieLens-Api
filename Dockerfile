# Gebruik een lichte Python base image
FROM python:3.11-slim

# Zet environment variabelen zodat Python output direct zichtbaar is
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Zet de werkmap in de container
WORKDIR /app

# Installeer de basisafhankelijkheden
RUN apt-get update && apt-get install -y --no-install-recommends 
    build-essential 
    && rm -rf /var/lib/apt/lists/*

# Update pip en installeer poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Kopieer dependency bestanden voor snellere builds via Docker cache
COPY pyproject.toml poetry.lock* /app/

# Voorkom dat poetry een virtual environment aanmaakt binnen de container
RUN poetry config virtualenvs.create false 
    && poetry install --no-interaction --no-ansi --only main

# Kopieer de rest van de broncode
COPY . /app/

# Open de poort waarop FastAPI draait
EXPOSE 8000

# Start de server via Uvicorn (of Gunicorn voor productie)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
