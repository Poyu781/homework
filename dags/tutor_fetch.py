try:

    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import pendulum
    from snapask_crawl import crawl_tutors
    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))


local_tz = pendulum.timezone("Asia/Taipei")

def get_tutors_from_snapask(**context):
    result = crawl_tutors.do_multiple_thread_to_store_data(crawl_tutors.fetch_tutors_data,10)
    context['ti'].xcom_push(key='crawl_result', value=result)



def insert_tutors_into_mysql(**context):
    crawl_result = context.get("ti").xcom_pull(key="crawl_result")
    if crawl_result :
        result = crawl_tutors.insert_tutors_info_mysql()
        context['ti'].xcom_push(key='insert_result', value=result)
    else:
        raise("It seems have some trouble when crawling")

def filter_and_store_elite_tutor(**context):
    tutor_insert_result = context.get("ti").xcom_pull(key="insert_result")
    if tutor_insert_result:
        crawl_tutors.get_elite_tutors()
        



with DAG(
        dag_id="get_snapask_elite_tutor",
        schedule_interval="20 20 * * *",
        default_args={
            "owner": "poyu",
            "retries": 1,
            "retry_delay": timedelta(minutes=1),
            "start_date": datetime(2021, 7, 21,tzinfo=local_tz),
        },
        catchup=False,
        ) as dag:

    get_tutors_from_snapask = PythonOperator(
        task_id="get_tutors_from_snapask",
        python_callable=get_tutors_from_snapask,
        provide_context=True,
    )
    insert_tutors_into_mysql = PythonOperator(
        task_id="insert_tutors_into_mysql",
        python_callable=insert_tutors_into_mysql,
        provide_context=True,
    )

    filter_and_store_elite_tutor = PythonOperator(
        task_id="filter_and_store_elite_tutor",
        python_callable=filter_and_store_elite_tutor,
        provide_context=True,
    )

get_tutors_from_snapask >> insert_tutors_into_mysql >> filter_and_store_elite_tutor


