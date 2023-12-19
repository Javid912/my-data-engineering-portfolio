from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'Javad',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='My avalin01 DAG',
    schedule_interval=timedelta(days=1),  # adjust this based on your scheduling needs
)

start_dag = DummyOperator(task_id='start_dag', dag=dag)
end_dag = DummyOperator(task_id='end_dag', dag=dag)

def sense_csv_file_function(**kwargs):
    # Your logic to sense the CSV file
    print("Sensing CSV file")

sense_csv_file = PythonOperator(
    task_id='sense_csv_file',
    python_callable=sense_csv_file_function,
    provide_context=True,
    dag=dag,
)

def sense_json_file_function(**kwargs):
    # Your logic to sense the JSON file
    print("Sensing JSON file")

sense_json_file = PythonOperator(
    task_id='sense_json_file',
    python_callable=sense_json_file_function,
    provide_context=True,
    dag=dag,
)

start_dag >> [sense_csv_file, sense_json_file] >> end_dag
