from dateutil import parser
from datetime import datetime, timedelta
from datetime import timezone
from airflow import DAG
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator


default_args = {
    'owner': 'batman',
    'retry_delay': timedelta(seconds=5),
    'depends_on_past': False,
    'start_date': parser.isoparse('2021-05-25T07:33:37.393Z').replace(tzinfo=timezone.utc)
}

example_dag = DAG(
    'airflow-dag',
    default_args=default_args, 
    schedule_interval='@daily', 
    catchup=False, 
    is_paused_upon_creation=False
)

spark_join_data = CDEJobRunOperator(
    connection_id='my-vc',
    task_id='read-join-write',
    retries=3,
    dag=example_dag,
    job_name='spark-read-write'
)

spark_read_data = CDEJobRunOperator(
    connection_id='my-vc',
    task_id='read',
    retries=3,
    dag=example_dag,
    job_name='spark-read'
)



spark_join_data >> spark_read_data