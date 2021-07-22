try:

    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime


    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))

from modules.test import test
import pendulum
local_tz = pendulum.timezone("Asia/Taipei")

def first_function_execute(**context):
    test()
    context['ti'].xcom_push(key='mykey', value="first_function_execute says Hello ")



def second_function_execute(**context):
    instance = context.get("ti").xcom_pull(key="mykey")
    print("I am in second_function_execute got value :{} from Function 1  ".format(instance))


with DAG(
        dag_id="first_dag",
        schedule_interval="52 10 * * *",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2021, 7, 21,tzinfo=local_tz),
        },
        catchup=False,
        ) as dag:

    first_function_execute = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute,
        provide_context=True,
        op_kwargs={"name":"Soumil Shah"}
    )

    second_function_execute = PythonOperator(
        task_id="second_function_execute",
        python_callable=second_function_execute,
        provide_context=True,
    )

first_function_execute >> second_function_execute


