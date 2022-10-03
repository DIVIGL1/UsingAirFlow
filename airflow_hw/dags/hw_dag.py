import datetime as dt
import logging
import os
import sys

from airflow.models import DAG
from airflow.operators.python import PythonOperator

path = os.path.expanduser('./airflow_hw')

# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

from modules.pipeline import pipeline_func
from modules.predict import predict_func

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule_interval="*/1 * * * *",
        default_args=args,
) as dag:
    pipeline_task = PythonOperator(
        task_id='model_creation',
        python_callable=pipeline_func,
        dag=dag,
    )
    predict_task = PythonOperator(
        task_id='price_prediction',
        python_callable=predict_func,
        dag=dag,
    )

    pipeline_task >> predict_task