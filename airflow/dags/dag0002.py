from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.sensors import GoogleCloudStorageObjectSensor

default_args = {
    'owner': 'Javad',
    'start_date': datetime(2023, 12, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcs_file_check_dag_2',
    default_args=default_args,
    description='Second DAG to check GCS file existence',
    schedule_interval=timedelta(days=1),  
)

# Define the bucket and file to check
bucket_name = 'avalin-bucket'
file_name_1 = 'avalin-bucket/Data/babak1.csv'
file_name_2 = 'avalin-bucket/Data/babak2.json'

# Create tasks to check file existence
check_file_1 = GoogleCloudStorageObjectSensor(
    task_id='sense_csv_file',
    bucket=bucket_name,
    object=file_name_1,
    mode='poke',
    poke_interval=600,
    timeout=600,
    soft_fail=True,
    dag=dag,
)

check_file_2 = GoogleCloudStorageObjectSensor(
    task_id='sense_json_file',
    bucket=bucket_name,
    object=file_name_2,
    mode='poke',
    poke_interval=600,
    timeout=600,
    soft_fail=True,
    dag=dag,
)
