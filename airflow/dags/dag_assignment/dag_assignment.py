
from airflow import DAG
from airflow.decorators import dag, task
from datetime import datetime

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryDeleteDatasetOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.bigquery_check_operator import BigQueryCheckOperator

default_args = {
    'owner': 'Javad',
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
    'retries': 1,
    }

with DAG(
    dag_id= 'gcs_file_check_dag_v05',
    default_args=default_args,
    description='DAG to check GCS file existence',
    schedule_interval="@once",  
) as dag:

    start_dag = DummyOperator(task_id='start_dag')
    end_dag = DummyOperator(task_id='end_dag')

    # Define the bucket and file to check
    bucket_csv = 'avalin-bucket'
    file_csv_1 = 'avalin-bucket/Data/babak1.csv'

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail.csv',
        dst='raw/online_retail.csv',
        bucket='javadsatoungar_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    # Create tasks to check file existence
    check_file_csv_1 = GoogleCloudStorageObjectSensor(
        task_id='sense_csv_file',
        bucket=bucket_csv,
        object=file_csv_1,
        mode='poke',
        poke_interval=600,
        timeout=600,
        soft_fail=True,
    )


    gcs_to_bq_file_1 = GCSToBigQueryOperator(
    task_id='gcs_to_bq_scv_1',
    bucket=bucket_csv, 
    source_objects=['avalin-bucket/Data/babak1.csv'],
    destination_project_dataset_table='my-new-gcp-project-406521.your_csv1.table_1', 
    create_disposition='CREATE_IF_NEEDED', 
    write_disposition='WRITE_TRUNCATE',
    #google_cloud_storage_conn_id='gcp',
    dag=dag,
    )

   # bq_check_running_average = BigQueryCheckOperator(
    #   sql="./sql/query_check_running_average.sql"

    #)

    start_dag >> check_file_csv_1 >> gcs_to_bq_file_1 >> end_dag
    #start_dag >> check_file_csv_1 >> gcs_to_bq_file_1 >> bq_check_running_average >> end_dag