
# YouTube Data Engineering Pipeline

> End-to-end cloud data engineering pipeline that extracts YouTube data through the YouTube Data API, orchestrates the workflow with Apache Airflow, stores raw data in Amazon S3, and transforms it into Bronze, Silver, and Gold Delta tables using Databricks and PySpark.

---

## 🚀 Project Overview

This project demonstrates a complete **modern data engineering workflow** for collecting, storing, transforming, and analyzing YouTube channel data.

The pipeline automatically:

1. Extracts YouTube channel and video metadata using the **YouTube Data API**
2. Validates and prepares the extracted data using **Python**
3. Uploads the raw dataset to **Amazon S3**
4. Uses **Apache Airflow** to orchestrate the end-to-end workflow
5. Triggers a **Databricks Job** through the Databricks REST API
6. Processes the raw data using **PySpark**
7. Creates **Bronze, Silver, and Gold** Delta tables
8. Produces aggregated analytics at the Gold layer

The pipeline has been tested with **500 YouTube video records**.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   YouTube Data API   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Python Extraction  │
                    │   API Data → JSON     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Apache Airflow    │
                    │   Workflow Orches.   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │      Amazon S3       │
                    │   Raw Data Storage   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Databricks Job     │
                    │    PySpark / Delta   │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌───────────┐    ┌───────────┐
        │  Bronze   │ →  │  Silver   │ →  │   Gold    │
        │   Layer   │    │   Layer   │    │   Layer   │
        └───────────┘    └───────────┘    └───────────┘
              │                │                │
              ▼                ▼                ▼
        Raw Structured      Cleaned &        Analytics
           Data             Validated          Data
````

---

## 🧰 Tech Stack

| Category                 | Technology             |
| ------------------------ | ---------------------- |
| Programming              | Python                 |
| Data Processing          | PySpark                |
| Data Source              | YouTube Data API v3    |
| Orchestration            | Apache Airflow         |
| Cloud Storage            | Amazon S3              |
| Data Processing Platform | Databricks             |
| Storage Format           | Delta Lake             |
| Data Architecture        | Medallion Architecture |
| API Integration          | REST API               |
| Environment              | Ubuntu WSL2            |
| Development              | VS Code                |
| Version Control          | Git / GitHub           |

---

## 🔄 End-to-End Pipeline

### 1. Data Extraction

The pipeline uses the **YouTube Data API v3** to retrieve channel and video information.

The extraction process collects up to **500 videos** and enriches the dataset with fields such as:

* Video ID
* Video title
* Channel title
* Published timestamp
* View count
* Like count
* Comment count
* Video duration
* Video definition
* Caption availability
* Category ID

The extracted data is stored locally as:

```text
raw/youtube_raw.json
```

---

### 2. Workflow Orchestration with Airflow

Apache Airflow manages the complete pipeline using a DAG named:

```text
youtube_data_pipeline
```

The DAG contains three main tasks:

```text
extract_youtube_data
        ↓
upload_to_s3
        ↓
trigger_databricks_job
```

#### Task 1 — Extract YouTube Data

Runs the Python extraction script and generates the raw JSON dataset.

#### Task 2 — Upload to Amazon S3

Uploads the raw JSON file to:

```text
s3://<bucket>/raw/youtube_raw.json
```

#### Task 3 — Trigger Databricks

Airflow triggers the Databricks Job through the Databricks REST API.

This keeps **Airflow as the workflow orchestrator** while Databricks is responsible for distributed data processing.

---

## ☁️ Amazon S3

Amazon S3 acts as the cloud storage layer for the raw data.

The pipeline stores the extracted dataset under:

```text
raw/
└── youtube_raw.json
```

This provides a persistent landing zone before the data enters the transformation layer.

---

# 🥉 Bronze Layer

The Bronze layer contains the raw data after it has been loaded into Databricks.

The pipeline:

* Reads JSON data from Amazon S3
* Parses the nested video structure
* Explodes the video records
* Selects relevant fields
* Stores the result as a Delta table

Bronze table:

```text
workspace.default.youtube_bronze
```

The Bronze layer is designed to preserve the extracted dataset in a structured format while keeping transformations minimal.

---

# 🥈 Silver Layer

The Silver layer contains cleaned and standardized data.

Transformations include:

* Removing duplicate videos
* Converting `published_at` into a timestamp
* Handling null numeric values
* Standardizing data types
* Preparing the dataset for analytics

Silver table:

```text
workspace.default.youtube_silver
```

This layer provides a cleaner and more reliable dataset for downstream analysis.

---

# 🥇 Gold Layer

The Gold layer contains business-oriented aggregated data.

The pipeline generates channel-level metrics including:

* Total videos
* Total views
* Total likes
* Total comments
* Average views
* Average likes
* Maximum views
* Minimum views

Gold table:

```text
workspace.default.youtube_gold
```

Example output structure:

| Metric           | Description             |
| ---------------- | ----------------------- |
| `channel_title`  | YouTube channel         |
| `total_videos`   | Number of videos        |
| `total_views`    | Total views             |
| `total_likes`    | Total likes             |
| `total_comments` | Total comments          |
| `avg_views`      | Average views per video |
| `avg_likes`      | Average likes per video |
| `max_views`      | Highest video views     |
| `min_views`      | Lowest video views      |

---

## 🔁 Databricks Job Integration

Databricks is configured as a separate Job rather than being manually executed from the notebook.

The Job:

```text
YouTube Data pipeline
```

executes the Databricks notebook responsible for the Bronze → Silver → Gold transformations.

Airflow triggers this Job using the Databricks REST API.

```text
Airflow
   │
   │ REST API
   ▼
Databricks Job
   │
   ▼
PySpark Notebook
   │
   ├── Bronze
   ├── Silver
   └── Gold
```

This separation gives the pipeline a clear responsibility model:

* **Airflow → orchestration**
* **S3 → raw storage**
* **Databricks → distributed processing**
* **Delta tables → processed data**

---

## 📊 Data Processing Results

The pipeline has been validated using:

```text
500 YouTube video records
```

The raw dataset is successfully loaded from Amazon S3 into Databricks and transformed through all three layers:

```text
S3 Raw Data
     ↓
Bronze
     ↓
Silver
     ↓
Gold
```

The Airflow workflow has also been successfully executed end-to-end:

```text
extract_youtube_data       ✅
upload_to_s3               ✅
trigger_databricks_job     ✅
```

---

# 📁 Project Structure

```text
YouTube DataBricks Pipeline/
│
├── airflow/
│   └── dags/
│       └── youtube_pipeline.py
│
├── dags/
│   └── youtube_pipeline.py
│
├── src/
│   ├── extract.py
│   └── s3_upload.py
│
├── databricks/
│   └── youtube_bronze
│
├── raw/
│   └── youtube_raw.json
│
├── bronze/
│
├── silver/
│
├── gold/
│
├── data/
│
├── tests/
│
├── requirements.txt
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

# ⚙️ How the Pipeline Works

### Step 1 — Extract

```text
YouTube API
     ↓
Python
     ↓
youtube_raw.json
```

### Step 2 — Store

```text
youtube_raw.json
     ↓
Amazon S3
     ↓
raw/youtube_raw.json
```

### Step 3 — Process

```text
Amazon S3
     ↓
Databricks
     ↓
PySpark
```

### Step 4 — Transform

```text
Bronze
  ↓
Silver
  ↓
Gold
```

### Step 5 — Orchestrate

```text
Apache Airflow
      ↓
Extract
      ↓
S3 Upload
      ↓
Databricks Job
```

---

# 🔐 Environment Variables

The project uses environment variables for credentials and configuration.

Create a `.env` file in the project root:

```env
YOUTUBE_API_KEY=<your_youtube_api_key>
YOUTUBE_CHANNEL_ID=<your_channel_id>

AWS_ACCESS_KEY_ID=<your_aws_access_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_key>
AWS_REGION=<your_aws_region>

S3_BUCKET_NAME=<your_s3_bucket>

DATABRICKS_HOST=<your_databricks_host>
DATABRICKS_TOKEN=<your_databricks_token>
```

### ⚠️ Security

Never commit `.env` or credentials to GitHub.

The `.gitignore` file should contain:

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
airflow/logs/
```

---

# 🚀 Running the Project

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd "YouTube DataBricks Pipeline"
```

---

## 2. Create Environment

Create a Python environment and install dependencies:

```bash
python -m venv venv
```

Activate it:

### Windows

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create `.env` and add the required API, AWS, S3, and Databricks configuration.

---

## 4. Test Data Extraction

Run:

```bash
python src/extract.py
```

This generates:

```text
raw/youtube_raw.json
```

---

## 5. Upload Data to S3

Run:

```bash
python src/s3_upload.py
```

The file will be uploaded to:

```text
raw/youtube_raw.json
```

inside the configured S3 bucket.

---

## 6. Run Airflow

Start Airflow and open:

```text
http://localhost:8080
```

Trigger:

```text
youtube_data_pipeline
```

Airflow executes:

```text
Extract → S3 Upload → Databricks Job
```

---

## 7. Databricks Processing

The Databricks Job processes the S3 dataset and creates:

```text
youtube_bronze
youtube_silver
youtube_gold
```

as Delta tables.

---

# 🧠 Key Data Engineering Concepts Demonstrated

This project demonstrates practical understanding of:

* ETL pipelines
* REST API ingestion
* Cloud object storage
* AWS S3
* Apache Airflow DAGs
* Workflow orchestration
* Databricks Jobs
* PySpark transformations
* Delta Lake
* Medallion Architecture
* Bronze / Silver / Gold layers
* Data cleansing
* Deduplication
* Data type conversion
* Null handling
* Aggregations
* REST API integration
* Cloud-to-cloud data workflows
* Environment variable management
* Pipeline dependency management

---

# 🎯 Why These Technologies?

### Why Apache Airflow?

Airflow is used to **orchestrate and monitor the workflow**.

Instead of manually running individual scripts, Airflow manages the dependency:

```text
Extraction
    ↓
S3 Upload
    ↓
Databricks Processing
```

---

### Why Amazon S3?

S3 provides durable cloud storage for the raw dataset and acts as the pipeline's **data landing zone**.

---

### Why Databricks?

Databricks provides a scalable environment for processing data with PySpark and storing transformed datasets using Delta Lake.

---

### Why Bronze, Silver, and Gold?

The Medallion Architecture separates data processing into clear stages:

```text
Bronze → Raw / Structured
Silver → Cleaned / Validated
Gold   → Aggregated / Analytics
```

This makes the pipeline easier to maintain, debug, and extend.

---

# 🛠️ Error Handling & Reliability

The pipeline uses several mechanisms to improve reliability:

* Airflow task dependencies
* HTTP response validation using `raise_for_status()`
* Environment-based configuration
* Explicit API request timeouts
* Separation of extraction and processing
* Airflow task-level monitoring
* Databricks Job execution status
* Deduplication in the Silver layer
* Null handling during transformation

If an upstream Airflow task fails, downstream tasks are not executed until the dependency is successfully completed.

---

# 📈 Possible Future Improvements

The current pipeline provides the complete core workflow. Potential future improvements include:

* Incremental data ingestion
* Partitioning large datasets
* Data quality validation with Great Expectations
* Airflow retry policies and alerting
* AWS IAM role-based authentication
* CI/CD using GitHub Actions
* Databricks Workflows with multiple tasks
* Dashboarding with Power BI
* Historical YouTube performance tracking
* Automated data-quality checks
* Monitoring and observability

---

# 💼 Resume Description

### YouTube Data Engineering Pipeline

**Python | PySpark | Apache Airflow | AWS S3 | Databricks | Delta Lake**

* Built an end-to-end YouTube data engineering pipeline using the YouTube Data API, Python, Apache Airflow, AWS S3, Databricks, and PySpark.
* Developed an Airflow DAG to orchestrate API extraction, S3 ingestion, and automated Databricks Job execution through REST API integration.
* Implemented Bronze, Silver, and Gold data layers using PySpark and Delta Lake, including deduplication, timestamp conversion, null handling, and analytical aggregations.
* Processed and validated a dataset of 500 YouTube videos and generated channel-level engagement metrics including views, likes, comments, and average performance.

---

# 🎤 Interview Explanation

> "I built an end-to-end YouTube data engineering pipeline to demonstrate how a real data workflow can be automated from source ingestion to analytics.
>
> I used the YouTube Data API to extract video-level metadata using Python. Apache Airflow orchestrates the workflow, where the first task extracts the data, the second uploads the raw JSON file to Amazon S3, and the third triggers a Databricks Job using the Databricks REST API.
>
> In Databricks, I used PySpark to implement a Bronze, Silver, and Gold architecture. The Bronze layer loads and structures the raw data, the Silver layer handles cleaning, deduplication, data types, and null values, and the Gold layer generates channel-level analytical metrics such as total views, likes, comments, and average views.
>
> This project helped me understand not only individual tools like Airflow, S3, and Databricks, but also how they work together as an end-to-end data engineering pipeline."

---

## 👩‍💻 Author

**Aashi Gupta**

B.Tech Computer Science Engineering

Data Engineering | Python | SQL | PySpark | Databricks | Apache Airflow

