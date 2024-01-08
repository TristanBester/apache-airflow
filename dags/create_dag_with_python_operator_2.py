from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def get_name(ti):
    ti.xcom_push(key="first_name", value="Jerry")
    ti.xcom_push(key="last_name", value="Friedman")


def get_age():
    return 30


def greet(ti):
    name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age")
    print(f"Hello World! My name is {name} {last_name}, age: {age}")


default_args = {
    "owner": "tristan",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    default_args=default_args,
    dag_id="our_dag_with_python_operator_v7",
    description="First DAG using the python operator",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="task_one",
        python_callable=greet,
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age,
    )

    [task2, task3] >> task1
