from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.S3_hook import S3Hook
import csv

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'start_dag',
    default_args=default_args,
    description='A simple DAG with S3 tasks',
    schedule_interval=timedelta(days=1),
)

# Define your S3 bucket and key (path within the bucket) here
s3_bucket_name = 'avalin-project'
s3_key_csv = 'path/to/your/csv/user-accessKeys.csv'

def sense_csv_file():
    s3_hook = S3Hook(aws_conn_id='aws_default')
    csv_object = s3_hook.get_key(s3_key_csv, s3_bucket_name)
    
    # Implement CSV sensing logic here
    csv_content = csv_object.get()['Body'].read().decode()
    print(f"Sensing CSV file: {csv_content}")

def end_dag():
    # Implement cleanup or end logic here
    print("End DAG")

start_dag = DummyOperator(task_id='start_dag', dag=dag)

csv_task = PythonOperator(
    task_id='sense_csv_file',
    python_callable=sense_csv_file,
    dag=dag,
)

end_dag = PythonOperator(
    task_id='end_dag',
    python_callable=end_dag,
    dag=dag,
)

start_dag >> csv_task >> end_dag
