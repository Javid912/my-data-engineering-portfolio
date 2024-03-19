
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

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType


default_args = {
    'owner': 'Javad',
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
    'retries': 1,
    }

with DAG(
    dag_id='gcs_dag_v06',
    default_args=default_args,
    description='DAG to upload file in gcp, from gcp to bigquery',
    schedule_interval="@once"
) as dag:

    start_dag = DummyOperator(task_id='start_dag')
    end_dag = DummyOperator(task_id='end_dag')

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail.csv',
        dst='raw/online_retail.csv',
        bucket='javadsatoungar_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )
#it has already tested and it is working

    # Create tasks to check file existence
#    check_file_csv_1 = GoogleCloudStorageObjectSensor(
#        task_id='sense_csv_file',
#        bucket=bucket_csv,
#        object=file_csv_1,
#        mode='poke',
#        poke_interval=600,
#        timeout=600,
#        soft_fail=True,
#    )


    creat_retile_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id = 'creat_retile_dataset',
        dataset_id = 'retail',
        gcp_conn_id='gcp'
    )
#already tested and it is working

# Use the BigQueryCreateEmptyTableOperator to create the table
#    create_table = BigQueryCreateEmptyTableOperator(
#        task_id="create_table",
#        dataset_id="retail",
#        table_id="raw_invoices",
#        gcp_conn_id='gcp',  
#        schema_fields= [
#            {"name": "InvoiceNo", "type": "STRING"},
#            {"name": "StockCode", "type": "STRING"},
#            {"name": "Description", "type": "STRING"},
#            {"name": "Quantity", "type": "INTEGER"},
#            {"name": "InvoiceDate", "type": "STRING"}, 
#            {"name": "UnitPrice", "type": "FLOAT"},
#            {"name": "CustomerID", "type": "FLOAT"},  
#            {"name": "Country", "type": "STRING"}
#        ], 
#    )
#testes and it worked, but it is not my first choise 

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://javadsatoungar_online_retail/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )
#task is tested and it is working, to use the GCSToBigQueryOperator there was problem importing the InvoiceDate
#becuse of bigquerys date data format requerments but the astro aql could do it without needing any data transformation 

    bq_check_running_average = BigQueryCheckOperator (
        task_id= "bq_check_running_average",
        conn_id='gcp',
        sql="./sql/query_check_running_average.sql"

        )
#Task is tested and it is working
start_dag >> upload_csv_to_gcs >> creat_retile_dataset >> gcs_to_raw >> bq_check_running_average >> end_dag