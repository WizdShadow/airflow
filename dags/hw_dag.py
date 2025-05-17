import datetime as dt
import os
import sys

from airflow.models import DAG
from airflow.operators.python import PythonOperator

dag_path = os.path.dirname(os.path.abspath(__file__))
# Путь к корню проекта (на уровень выше dags)
project_path = os.path.join(dag_path, '..')

# Добавляем путь проекта в PYTHONPATH
sys.path.insert(0, project_path)

from modules.pipeline import pipeline
from modules.predict import predict

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
        dag_id='car_price_prediction',
        schedule="00 15 * * *",
        default_args=args,
) as dag:
    pipeline = PythonOperator(
        task_id='pipeline',
        python_callable=pipeline,
        dag=dag
    )
    predict = PythonOperator(
        task_id='predict',
        python_callable=predict,
        dag=dag
    )

    pipeline >> predict
