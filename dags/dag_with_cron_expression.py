from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_cron_expression_v2",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="1 0 * * *",
    catchup=True,
) as dag:
    task_1 = BashOperator(
        task_id="task_1",
        bash_command='echo "This is a simple test task"',
    )
