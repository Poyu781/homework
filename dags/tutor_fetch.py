try:
    # Airflow
    from airflow import DAG
    print(1)
    from airflow.operators.python_operator import PythonOperator
    print(2)
    from airflow.models import TaskInstance
    print(3)
    # Modules
    from datetime import datetime,timedelta
    print(4)
    import pendulum
    print(5)
    from modules.mail_notification import send_email
    
    print(6)
    from snapask_crawl import crawl_tutors
    
    print(7)
    print("All Dag modules are ok ......")
except Exception as e:
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)

local_tz = pendulum.timezone("Asia/Taipei")
default_args = { "owner": "poyu",
                "retries": 1,
                "retry_delay": timedelta(minutes=1),
                "start_date": datetime(2021, 7, 21,tzinfo=local_tz)}


def get_tutors_from_snapask(**context):
    result = crawl_tutors.do_multiple_thread_to_store_data(crawl_tutors.fetch_tutors_data,15)
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
        
def check_status(**context):
    date = context['execution_date']
    ti = TaskInstance(filter_and_store_elite_tutor, date) #my_task is the task you defined within the DAG rather than the task_id (as in the example below: check_success_task rather than 'check_success_days_before') 
    state = ti.current_state()
    if state == 'success':
        title = f"Success Notification : tutor_elite_dag-{str(date)}"
        text = "tutor_elite_dag have already done"
    else :
        title = f"Fail Notification : tutor_elite_dag-{str(date)}"
        text = "tutor_elite_dag is failed,please check airflow"
    send_email(title,text)


with DAG(
        dag_id="get_snapask_elite_tutor",
        schedule_interval="00 8 * * *",
        default_args=default_args,
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
    check_status = PythonOperator(
        task_id="check_status",
        python_callable=check_status,
        provide_context=True,
        trigger_rule="all_done",
    )

    get_tutors_from_snapask >> insert_tutors_into_mysql >> filter_and_store_elite_tutor >> check_status


