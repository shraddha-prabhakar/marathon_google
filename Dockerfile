steps:
  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "gcr.io/$PROJECT_ID/daily-tech", "."]

  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/daily-tech"]

images:
  - gcr.io/$PROJECT_ID/daily-tech
