from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator  # type: ignore[reportMissingImports]

import sys
import os
import requests
from dotenv import load_dotenv

PROJECT_DIR = "/mnt/d/DE PROJECT/YouTube DataBricks Pipeline"

sys.path.insert(0, os.path.join(PROJECT_DIR, "src"))

from extract import main as extract_youtube_data
from s3_upload import upload_to_s3

load_dotenv(os.path.join(PROJECT_DIR, ".env"))


def run_extraction():
    os.chdir(PROJECT_DIR)
    extract_youtube_data()


def run_s3_upload():
    os.chdir(PROJECT_DIR)
    upload_to_s3()


def trigger_databricks_job():
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")

    job_id = 349454099880953

    url = f"{host}/api/2.2/jobs/run-now"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={"job_id": job_id},
        timeout=60,
    )

    response.raise_for_status()

    print("Databricks Job triggered successfully!")
    print(response.json())


with DAG(
    dag_id="youtube_data_pipeline",
    start_date=datetime(2026, 9, 24),
    schedule=None,
    catchup=False,
    tags=["youtube", "etl", "s3", "databricks"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_youtube_data",
        python_callable=run_extraction,
    )

    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=run_s3_upload,
    )

    databricks_task = PythonOperator(
        task_id="trigger_databricks_job",
        python_callable=trigger_databricks_job,
    )

    extract_task >> upload_task >> databricks_task