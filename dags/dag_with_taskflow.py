## Taskflow API

from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="dag_with_taskflow_v3",
    default_args=default_args,
    start_date=datetime(2024, 1, 8),
    schedule_interval="@daily",
)
def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "Jerry",
            "last_name": "Fridman",
        }

    @task()
    def get_age():
        return 19

    @task()
    def greet(name, last_name, age):
        print(f"Hello {name} {last_name}, you are {age} years old!")

    name_dict = get_name()
    age = get_age()
    greet(name_dict["first_name"], name_dict["last_name"], age)


hello_world_etl()
