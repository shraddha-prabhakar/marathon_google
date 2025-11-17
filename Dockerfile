<<<<<<< HEAD
FROM python:3.11-slim
=======
steps:
  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "gcr.io/$PROJECT_ID/daily-tech", "."]
>>>>>>> 39312bdaa5d43ce8be1f6efd01d23b2cf0700a34

<<<<<<< HEAD
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

=======
  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/daily-tech"]

images:
  - gcr.io/$PROJECT_ID/daily-tech

>>>>>>> 39312bdaa5d43ce8be1f6efd01d23b2cf0700a34