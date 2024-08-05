from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.hooks.postgres_hook import PostgresHook
import utils
from datetime import datetime

def get_schedule_interval(dag_id):
    

    conn = utils.get_db_conn()

    cursor = conn.cursor()

    cursor.execute("SELECT Crontab FROM recon.AirflowAgendamento")
    
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

dag_id = 'minha_dag'
schedule_interval = get_schedule_interval(dag_id)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2024, 4, 23)
}

with DAG(
    dag_id='minha_dag',
    default_args=default_args,
    description='Uma DAG de exemplo',
    schedule_interval=schedule_interval
) as dag:

    start_task = DummyOperator(task_id='start_task')

    end_task = DummyOperator(task_id='end_task')

    start_task >> end_task
