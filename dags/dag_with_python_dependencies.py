from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def list_version():
    import sklearn

    print(f"sklearn version: {sklearn.__version__}")


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_python_dependencies",
    default_args=default_args,
    start_date=datetime(2024, 1, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task_1 = PythonOperator(
        task_id="list_verion",
        python_callable=list_version,
    )
