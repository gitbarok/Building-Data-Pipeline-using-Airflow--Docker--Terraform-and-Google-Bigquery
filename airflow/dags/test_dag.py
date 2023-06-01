from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from helpers.scrape import scrape_jtiulm
from helpers.local_to_bq import load_to_bq


args = {
    "owner": "mubarok",
    "email": ["mubarok@gmail.com"],
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="test_dag",
    default_args=args,
    schedule_interval="0 9 * * 0",
    start_date=datetime(2023, 5, 30),
    dagrun_timeout=timedelta(minutes=60),
    max_active_runs=1,
)

scrape_jtiulm_task = PythonOperator(
    task_id="scrape_jtiulm_task",
    python_callable=scrape_jtiulm,
    op_kwargs={"output_file_name": "scrape_jtiulm_{{ ds }}.csv"},
    dag=dag,
)

local_to_bq = PythonOperator(
    task_id="local_to_bq",
    python_callable=load_to_bq,
    op_kwargs={"filename": "scrape_jtiulm_{{ ds }}.csv"},
    dag=dag,
)

delete_local_file = BashOperator(
    task_id="delete_local_file",
    bash_command="rm -rf scrape_jtiulm_{{ ds }}.csv",
    dag=dag,
)


scrape_jtiulm_task >> local_to_bq >> delete_local_file
