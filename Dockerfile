FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp .streamlit/config.toml ~/.streamlit/config.toml
WORKDIR /app
ENTRYPOINT ["streamlit", "run", "main.py","--server.port=80"]





