from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_with_postgres_operator_v5",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    task_1 = PostgresOperator(
        task_id="create_postgres_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            create table if not exists dag_runs(
                dt date,
                dag_id character varying(250),
                primary key (dt, dag_id)
            ) 
        """,
    )

    task_2 = PostgresOperator(
        task_id="delete_from_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """,
    )

    task_3 = PostgresOperator(
        task_id="insert_into_table",
        postgres_conn_id="postgres_localhost",
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ds}}', '{{dag.dag_id}}');
        """,
    )

    task_1 >> task_2 >> task_3
