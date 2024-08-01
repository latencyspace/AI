from google.cloud import bigquery
import pandas as pd

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "andong-24-adv-idv-130.test_data.test_table"
# Construct a DataFrame from the data you want to load.
data = [
    (pd.to_datetime("2023-11-22 10:30:00"), 25.5, 60.2),
    (pd.to_datetime("2023-11-22 11:00:00"), 26.1, 58.7),
    # ...
]
schema = [
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("temperature", "FLOAT"),
    bigquery.SchemaField("humidity", "FLOAT"),
]
dataframe = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])

# Load the data into a new table.
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,   # 기존 데이터를 삭제하고 덮어쓰기
job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)

job.result()  # Wait for the job to complete.

print("Loaded {} rows.".format(job.output_rows))