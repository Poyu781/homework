from modules.mysql_module import SQL
from modules.crawl import fetch_data
from config import GCP_MYSQL_HOST,GCP_MYSQL_PASSWORD,GCP_MYSQL_USER,BASE_DIR
import os,json
import threading,time
from datetime import datetime

today_date = datetime.today().date()
str_today = str(today_date)
snapask_db = SQL(user=GCP_MYSQL_USER,password=GCP_MYSQL_PASSWORD,host=GCP_MYSQL_HOST,database="snapask")
def fetch_tutors_data(url,collect_list):
    result = fetch_data(url,"json")
    collect_list.extend(result['data']['tutors'])

def do_multiple_thread_to_store_data(fun,loop_num):
    result_data_collections = []
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

def insert_tutor_personal_info(data):
    tutors_info_insert_list = []
    tutors_rating_insert_list = []
    for tutor in data :
        single_tutor_list = [tutor['id'],tutor['first_name'],tutor['last_name'],
                            tutor['username'],tutor['display_name'],tutor['profile_pic_url'],tutor['school']]
        tutors_info_insert_list.append(single_tutor_list)
        single_rating_list = [tutor['id'],tutor['rating'],tutor['answered_count'],str_today]
        tutors_rating_insert_list.append(single_rating_list)
    snapask_db.bulk_execute("INSERT IGNORE INTO `tutors_basic_info`(`id`, `first_name`, `last_name`, `user_name`, `display_name`, `pic_url`, `school`) VALUES (%s,%s,%s,%s,%s,%s,%s)",tutors_info_insert_list)
    snapask_db.bulk_execute("INSERT INTO `tutors_ratings`(`tutor_id`, `rating`, `answered_count`, `update_date`) VALUES (%s,%s,%s,%s)",tutors_rating_insert_list)

def insert_tutor_subject_info(data):
    subject_set = set()
    tutors_subject_relation_list = []
    for tutor in data :
        single_tutor_subject_list = [tutor['id']]
        for subject in tutor['top_answered_subjects']:
            subject_set.add(subject)
            single_tutor_subject_list.append(subject)
        tutors_subject_relation_list.append(single_tutor_subject_list)
    snapask_db.bulk_execute("INSERT IGNORE INTO `subjects`( `subject_name`) VALUES (%s)",list(subject_set))
    subject_data = snapask_db.fetch_list("SELECT * FROM `subjects`")
    subject_dict = {i[1]:i[0] for i in subject_data}

    insert_subject_relation_list = []
    for i in tutors_subject_relation_list :
        for index in range(1,len(i)) :
            insert_subject_relation_list.append([i[0],subject_dict[i[index]]])
    snapask_db.bulk_execute("INSERT IGNORE INTO `subject_tutor_relation`(`tutor_id`, `subject_id`) VALUES (%s,%s)",insert_subject_relation_list)

def insert_tutors_into_mysql():
    file_path = os.path.join(BASE_DIR, f'data/tutors_2021-07-21.json')
    with open(file_path,"r") as f :
        data = f.read()
        json_tutors_data = json.loads(data)
    insert_tutor_personal_info(json_tutors_data)
    insert_tutor_subject_info(json_tutors_data)
    

def get_elite_tutors():
    snapask_db = SQL(user=GCP_MYSQL_USER,password=GCP_MYSQL_PASSWORD,host=GCP_MYSQL_HOST,database="snapask")
    elite_list = snapask_db.fetch_list("SELECT tutor_id from tutors_ratings where rating >= 4.8 and answered_count >= 100")
    insert_elite_list = [i[0] for i in elite_list]
    snapask_db.bulk_execute("INSERT IGNORE INTO `elite_tutors`(`tutor_id`) VALUES (%s)",insert_elite_list)


if __name__ == "__main__":
    # insert_data_into_mysql
#     r = snapask_db.fetch_dict('''
#     SELECT tutors_basic_info.id,tutors_basic_info.display_name,tutors_basic_info.pic_url,tutors_basic_info.school,tutors_ratings.rating,tutors_ratings.answered_count,answered_subject.subject_list 
# FROM tutors_basic_info INNER JOIN tutors_ratings ON tutors_ratings.tutor_id = tutors_basic_info.id INNER JOIN
# (SELECT subject_table.tutor_id,
#         GROUP_CONCAT(subject_table.subject_name ) AS 'subject_list'
# FROM (SELECT subjects.subject_name ,subject_tutor_relation.tutor_id FROM subjects INNER JOIN subject_tutor_relation ON subjects.id = subject_tutor_relation.subject_id )AS subject_table 
# GROUP BY subject_table.tutor_id) AS answered_subject
# ON answered_subject.tutor_id = tutors_basic_info.id
#     ''')

    # insert_tutors_into_mysql()

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

# SELECT tutors_basic_info.id,tutors_basic_info.display_name,tutors_basic_info.pic_url,tutors_basic_info.school,tutors_ratings.rating,tutors_ratings.answered_count,answered_subject.subject_list 
# FROM tutors_basic_info INNER JOIN tutors_ratings ON tutors_ratings.tutor_id = tutors_basic_info.id INNER JOIN
# (SELECT subject_table.tutor_id,
#         CONCAT("[", GROUP_CONCAT(subject_table.subject_name ), "]") AS 'subject_list'
# FROM (SELECT subjects.subject_name ,subject_tutor_relation.tutor_id FROM subjects INNER JOIN subject_tutor_relation ON subjects.id = subject_tutor_relation.subject_id )AS subject_table 
# GROUP BY subject_table.tutor_id) AS answered_subject
# ON answered_subject.tutor_id = tutors_basic_info.id