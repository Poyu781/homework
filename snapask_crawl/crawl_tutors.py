from modules.mysql_module import SQL
from modules.crawl import fetch_data
from config import GCP_MYSQL_HOST,GCP_MYSQL_PASSWORD,GCP_MYSQL_USER,BASE_DIR
import os,json
import threading,time
from datetime import datetime
#"https://api.snapask.co/api/v3/web/tutor_list?region_name=tw&filter_name=&page=1&lang=zh-TW"
today_date = datetime.today().date()
str_today = str(today_date)
result_data_collections = []
def fetch_tutors_data(url,collect_list):
    result = fetch_data(url,"json")
    collect_list.extend(result['data']['tutors'])

def do_multiple_thread_to_store_data(fun,loop_num):
    threads = []
    for i in range(1,loop_num+1):
        url = f"https://api.snapask.co/api/v3/web/tutor_list?region_name=tw&filter_name=&page={i}&lang=zh-TW"
        threads.append(threading.Thread(target = fun, args = (url,result_data_collections)))
        time.sleep(0.05)
        threads[-1].start()
    for i in threads:
        i.join()
    file_path = os.path.join(BASE_DIR, f'data/tutors_{str_today}.json')
    with open(file_path,"w") as f :
        f.write(json.dumps(result_data_collections))

def insert_data_into_mysql():
    snapask_db = SQL(user=GCP_MYSQL_USER,password=GCP_MYSQL_PASSWORD,host=GCP_MYSQL_HOST,database="snapask")
    file_path = os.path.join(BASE_DIR, f'data/tutors_2021-07-21.json')
    with open(file_path,"r") as f :
        data = f.read()
        json_tutors_data = json.loads(data)
    subject_set = set()
    tutors_info_insert_list = []
    tutors_rating_insert_list = []
    for tutor in json_tutors_data :
        single_tutor_list = [tutor['id'],tutor['first_name'],tutor['last_name'],
                            tutor['username'],tutor['display_name'],tutor['profile_pic_url'],tutor['school']]
        tutors_info_insert_list.append(single_tutor_list)
        single_rating_list = [tutor['id'],tutor['rating'],tutor['answered_count']]
        tutors_rating_insert_list.append(single_rating_list)
        for subject in tutor['top_answered_subjects']:
            subject_set.add(subject)
    print(tutors_info_insert_list)
    print(tutors_rating_insert_list)
    # snapask_db.bulk_execute("INSERT IGNORE INTO `subjects`(`subject_name`) VALUES(%s)",list(subject_set))
    # file_path = os.path.join(BASE_DIR, 'data/tutors_2020_12_15.json')

    # print(snapask_db.fetch_list("select * from tutors_basic_info"))


if __name__ == "__main__":
    insert_data_into_mysql()
    # fetch_tutors_data()
    # file_path = os.path.join(BASE_DIR, f'data/tutors_{str_today}.json')
    # with open(file_path,"r") as f :
    #     x = f.read()
    #     r = json.loads(x)
    #     print(r[0])
    # do_multiple_thread_to_store_data(fetch_tutors_data,3)
    # fetch_tutors_data(result_data_collections)
    # fetch_tutors_data(result_data_collections)
    # print(result_data_collections)