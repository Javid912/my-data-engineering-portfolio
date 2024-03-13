from airflow import DAG
from airflow.utils.dates import days_ago

my_dag = DAG(
    'my_very_first_dag',
    description='My first DAG created with DataScientest',
    tags=['tutorial', 'datascientest'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2),
    }
)

#Defining a task
#We will define a very simple single task that displays the time,
#along with a message in the standard output. We will therefore use a 
# PythonOperator. The following lines define such a Task.

from airflow.operators.python import PythonOperator
import datetime

# definition of the function to execute
def print_date_and_hello():
    print(datetime.datetime.now())
    print('Hello from Airflow')


my_task = PythonOperator(
    task_id='TEST',
    python_callable=print_date_and_hello,
    dag=my_dag
)