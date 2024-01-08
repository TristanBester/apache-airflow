from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "tristan",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="our_first_dag_v5",
    default_args=default_args,
    description="This is our first DAG",
    start_date=datetime(2024, 1, 1, 2),
    schedule_interval="@daily",
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo Hello World! This is the first task.",
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command='echo "I am the second task. I will run after task 1."',
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command='echo "I am the third task. I will run after task 1 along with task 2."',
    )

    task1 >> [task2, task3]
