from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

import re 
import time
from datetime import datetime
import pendulum
import os,json
import math

from config import BASE_DIR

local_tz = pendulum.timezone("Asia/Taipei")
today_date = datetime.now(tz=local_tz).date()
str_today = str(today_date)

def crawl_tutor_by_selenium(tutor_amount):
    # driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.101").install())
    driver_path = os.path.join(BASE_DIR, "chromedriver")
    driver = webdriver.Chrome(driver_path)
    driver.get("https://snapask.com/zh-tw/tutors#navigation")
    click_times = math.ceil(tutor_amount/12)+1
    
    # click more button for web rendering data
    for i in range(1,click_times):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[@id='app']/div/div/div/section[2]/button/div/div[1]"))
        )
        element.click()

    store_data = []
    for i in range(1,tutor_amount+1):
        # get all data inside the tutor div
        tutor_dom = driver.find_elements_by_xpath(f"//*[@id='app']/div/div/div/section[2]/div[2]/div[{i}]")
        data = tutor_dom[0].text.split("\n")
        # get img src and tutor_id by img tag
        image = driver.find_element_by_xpath(f"//*[@id='app']/div/div/div/section[2]/div[2]/div[{i}]/img")
        url = image.get_attribute("src")
        id_data = re.search(r'pics.*?o', url,flags=re.M)[0][5:-2]
        tutor_id = int(id_data.replace("/","",3))
        
        tutor_info_dict = {}
        tutor_info_dict['top_answered_subjects'] = []
        tutor_info_dict['profile_pic_url'] = url
        tutor_info_dict['id'] = tutor_id
        
        for index in range(len(data)) :
            text_value = data[index]
            if index == 0  :
                tutor_info_dict['display_name'] = text_value
            elif index == 1 :
                tutor_info_dict['rating'] = float(text_value)
            elif index == 2 :
                tutor_info_dict["answered_count"] = int(text_value.replace("(","").replace(")",""))
            elif index == 3 :
                tutor_info_dict['school'] = text_value
            elif index >= 4 :
                tutor_info_dict['top_answered_subjects'].append(text_value) 
        tutor_info_dict['last_name'] =''
        tutor_info_dict['first_name'] =''
        store_data.append(tutor_info_dict)

    file_path = os.path.join(BASE_DIR, f'data/tutors_{str_today}.json')
    with open(file_path,"w") as f :
        f.write(json.dumps(store_data,ensure_ascii=False))

    driver.quit()
    return True






if __name__ == "__main__" :
    crawl_tutor_by_selenium(35)
