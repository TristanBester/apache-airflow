from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def get_name(ti):
    return "Jerry"


def greet(age, ti):
    # Retrieve the return value of the task with task_id='get_name'
    name = ti.xcom_pull(task_ids="get_name")
    print(f"Hello World! My name is {name}, and I am {age} years old.")


default_args = {
    "owner": "tristan",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    default_args=default_args,
    dag_id="our_dag_with_python_operator_v4",
    description="First DAG using the python operator",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="task_one",
        python_callable=greet,
        op_kwargs={
            "age": 30,
        },
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
    )

    task2 >> task1
