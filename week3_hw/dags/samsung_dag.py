import os
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.samsung_pred import get_stock_data, set_stock_data, train_model_predict

seoul_time = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

default_args = {
    'owner': 'junhy',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='내일의 삼성전자 주가 예측',
    schedule_interval=timedelta(minutes=10),
    start_date=pendulum.datetime(2023, 11, 6, tz=seoul_time),
    catchup=False,
    tags=['samsung', 'stock', 'prediction']
) as dag:
    get_stock_data_task = PythonOperator(
        task_id='get_stock_data_task',
        python_callable=get_stock_data,
    )

    set_stock_data_task = PythonOperator(
        task_id='set_stock_data_task',
        python_callable=set_stock_data,
    )

    train_model_predict_task = PythonOperator(
        task_id='train_model_predict_task',
        python_callable=train_model_predict,
    )
    
    get_stock_data_task >> set_stock_data_task >> train_model_predict_task