FROM python:3.12-slim

WORKDIR /repo
COPY requirements.txt /repo/requirements.txt
RUN pip install --no-cache-dir -r /repo/requirements.txt

COPY . /repo

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
