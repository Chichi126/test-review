### 📊 **Project Title**: Customer Review Pipeline on Azure with Unity Catalog and Databricks

![](https://github.com/Chichi126/test-review/blob/main/azure%20(5).jpg)


#### Project Overview

##### Aim

The goal of this project is to build a scalable, secure, and well-governed data pipeline to process customer review data using Azure Data Lake Storage, Unity Catalog, and Databricks. 

The pipeline ingests raw review data, transforms and cleans it in Databricks using PySpark, and stores the processed data in a structured format for analytics and reporting.

##### Business Importance

Customer feedback is a valuable asset for any company seeking to improve product offerings, customer experience, and brand reputation. This project empowers cross-functional teams, including Marketing, Product, and Data Teams, with clean, timely, and accessible customer sentiment data. By implementing data governance through Unity Catalog and ensuring secure access controls, this solution supports regulatory compliance, promotes collaboration, and accelerates data-driven decision-making across the organization.


##### Features

Secure and scalable data ingestion from API or file sources

Use of cloud-native data platforms (Azure Storage, Databricks)

Data governance with Unity Catalog for data governance, access control, and security

Incremental transformation with partitioned Delta Lake

Metadata and lineage tracking

Optimized output for downstream analytics and ML models


##### Stack And Technologies Used

Azure Data Lake Storage Gen2

Azure Unity Catalog

Databricks (PySpark, Auto Loader, Delta Lake)

Azure Active Directory (for RBAC)

GitHub (Version Control)



### 🔧 **Step-by-Step Implementation**

#### **1. Data Ingestion**

* Collected raw customer reviews from a mock API (or CSV file dump).
* Ingested the data into **Azure Data Lake Storage Gen2 (Bronze Layer)** using a secure **abfss path**.
* Directory: `abfss://<container>@<storage_account>.dfs.core.windows.net/bronze/customer_reviews/`

#### **2. Set Up Unity Catalog**

* Registered the **Azure storage** and linked it to Unity Catalog using **external locations** and **storage credentials**.
* Created a managed **schema and tables** under Unity Catalog for fine-grained access.
* Ensured **RBAC** and **data lineage tracking** were enabled for governance.

#### **3. Transformation in Databricks**

* Created a **notebook in Databricks** to process raw data using **PySpark**.
* Applied transformations:

  * Removed null entries and empty reviews
  * Extracted sentiment features (e.g., polarity, review length)
  * Standardized column formats and corrected data types
* Added **ingestion and processing timestamps**.

#### **4. Saved to Silver Layer**

* Saved the cleaned data back to **Azure Data Lake (Silver Layer)** in **Delta format**:

  * `abfss://<container>@<storage_account>.dfs.core.windows.net/silver/customer_reviews/`
* Partitioned by `review_date` for query efficiency.

#### **5. Enabled Team Access**

* Registered the transformed Delta table under **Unity Catalog** as a shared resource:

  * `catalog.analytics.customer_reviews_silver`
* Assigned access permissions using Unity Catalog policies, so **other data teams (BI, ML, etc.)** could consume the table directly.

---

📘 Step-by-Step Implementation

✅ Step 1: API Data Ingestion
Write code in vscode to upload data to Azure Storage 
[View script.py](https://github.com/Chichi126/test-review/blob/main/script.py)

✅ Step 2: Define Raw Path in Databricks

raw_path = "abfss://yourcontainer@yourstorage.dfs.core.windows.net/bronze"

✅ Step 3: Stream Ingestion with Auto Loader
 
 Ingest Excel Files:  you'll need to use the com.crealytics.spark.excel package. First, ensure the library is attached to your cluster:

 Maven: com.crealytics:spark-excel_2.12:0.13.5

csv_df = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .option("cloudFiles.schemaLocation", "abfss://.../schemas/crypto_csv") \
    .load(raw_path)

excel_df = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "binaryFile") \
    .option("cloudFiles.schemaLocation", "abfss://.../schemas/crypto_excel") \
    .load(raw_path) \
    .filter("path LIKE '%.xlsx'") \
    .selectExpr("path as file_path")


✅ Step 4: Data Transformation

Extract useful fields (e.g., rating, sentiment, timestamp)

Apply data cleaning and typecasting

Add partitioning columns (date_partition, hour_partition)

df_final = df_raw.withColumn("date_partition", to_date("ingest_timestamp"))

✅ Step 5: Save to Silver Layer with Delta Format

silver_path = "abfss://.../silver/customer_reviews"

df_final.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "abfss://.../checkpoints/reviews") \
    .partitionBy("date_partition") \
    .start(silver_path)

✅ Step 6: Unity Catalog Registration

Create external location and schema

Register silver Delta table in Unity Catalog

CREATE TABLE reviews_catalog.silver.customer_reviews
USING DELTA
LOCATION 'abfss://.../silver/customer_reviews';

🎓 Learning Outcome

This project demonstrates practical skills in designing cloud-native data pipelines using Azure and Databricks. It emphasizes data governance, secure access, and scalable processing, aligning with enterprise-grade data engineering roles.

📖 How to Run

Clone this repo

Configure Azure credentials and Unity Catalog access

Deploy notebooks on Databricks

Execute ingestion and transformation pipelines step-by-step


##### Create Pipelines in ADF

Pipeline Name: Ingest_CSV_Excel_Pipeline

[Databricks Notebook Activity - Ingest CSV]

Name: Run_CSV_Notebook

Linked service: Databricks_LinkedService

Path: /path/to/csv_notebook

Parameters (if any): Pass storage paths if parameterized

[Databricks Notebook Activity - Ingest Excel]

Name: Run_Excel_Notebook

Linked service: Databricks_LinkedService

Path: /path/to/excel_notebook

[Success Dependency]

Link the CSV notebook activity → Excel notebook activity to run sequentially.

###### Trigger the Pipeline
Add a Trigger to schedule it daily or run manually.

Monitor execution via ADF Monitor tab.



##### Project Outcome & Business Benefits
This project successfully delivers a production-grade data pipeline that ingests customer review data in both CSV and Excel formats using Azure Data Factory and Databricks. The pipeline transforms and stores the data in partitioned Delta tables within Azure Data Lake, all governed under Unity Catalog for secure, enterprise-wide access.

Key benefits to the company include:

Accelerated access to clean, analytics-ready customer feedback for product and marketing teams

Unified governance and access control via Unity Catalog, supporting compliance with NDPR and NIST standards

Scalable and modular architecture designed to support future data sources with minimal effort

Streamlined orchestration using Azure Data Factory, enabling automation, reliability, and monitoring across the pipeline

This solution enables timely insights, improves operational efficiency, and supports data-driven decision-making across the organization.

