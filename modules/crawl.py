import json
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
import threading, time
import requests
import tenacity

ua = UserAgent(verify_ssl=False)
ip_list = [
    'http://tihyjcyk:sr9mbjac4xab@193.8.231.209:9215',
    'http://tihyjcyk:sr9mbjac4xab@107.152.177.67:6087',
    'http://tihyjcyk:sr9mbjac4xab@45.57.168.196:7200',
    'http://tihyjcyk:sr9mbjac4xab@138.122.194.254:7330',
    'http://tihyjcyk:sr9mbjac4xab@104.144.26.137:8667',
    'http://tihyjcyk:sr9mbjac4xab@45.154.244.123:8161',
    'http://tihyjcyk:sr9mbjac4xab@185.102.50.157:7240',
    'http://tihyjcyk:sr9mbjac4xab@5.154.253.240:8498',
    'http://tihyjcyk:sr9mbjac4xab@185.242.94.107:6192',
    'http://tihyjcyk:sr9mbjac4xab@5.154.253.113:8371',
    'http://tihyjcyk:sr9mbjac4xab@185.242.95.181:6522',
    'http://tihyjcyk:sr9mbjac4xab@5.157.130.161:8165',
    'http://tihyjcyk:sr9mbjac4xab@194.33.61.45:8628',
    'http://tihyjcyk:sr9mbjac4xab@45.130.60.93:9620',
    'http://tihyjcyk:sr9mbjac4xab@194.33.61.44:8627',
    'http://tihyjcyk:sr9mbjac4xab@45.154.84.190:8241',
    'http://tihyjcyk:sr9mbjac4xab@91.246.195.28:6797',
    'http://tihyjcyk:sr9mbjac4xab@45.137.80.64:9084',
    'http://tihyjcyk:sr9mbjac4xab@37.35.40.21:8111',
    'http://tihyjcyk:sr9mbjac4xab@64.43.90.245:6760',
    'http://tihyjcyk:sr9mbjac4xab@45.140.14.98:8114',
    'http://tihyjcyk:sr9mbjac4xab@45.136.231.236:7292',
    'http://tihyjcyk:sr9mbjac4xab@182.54.239.228:8245',
    'http://tihyjcyk:sr9mbjac4xab@176.116.231.240:7582',
    'http://tihyjcyk:sr9mbjac4xab@64.43.90.91:6606',
    'http://tihyjcyk:sr9mbjac4xab@193.151.160.34:8121',
    'http://tihyjcyk:sr9mbjac4xab@193.27.10.54:6139',
    'http://tihyjcyk:sr9mbjac4xab@45.136.231.128:7184',
    'http://tihyjcyk:sr9mbjac4xab@45.72.55.91:7128',
    'http://tihyjcyk:sr9mbjac4xab@185.102.48.143:6225',
    'http://tihyjcyk:sr9mbjac4xab@182.54.239.8:8025',
    'http://tihyjcyk:sr9mbjac4xab@45.94.47.183:8227',
    'http://tihyjcyk:sr9mbjac4xab@45.140.13.98:9111',
    'http://tihyjcyk:sr9mbjac4xab@185.102.48.186:6268',
    'http://tihyjcyk:sr9mbjac4xab@194.31.162.173:7689',
    'http://tihyjcyk:sr9mbjac4xab@45.131.212.36:6085',
    'http://tihyjcyk:sr9mbjac4xab@45.87.249.71:7649',
    'http://tihyjcyk:sr9mbjac4xab@5.154.253.123:8381',
    'http://tihyjcyk:sr9mbjac4xab@45.72.55.118:7155',
    'http://tihyjcyk:sr9mbjac4xab@185.242.94.47:6132',
    'http://tihyjcyk:sr9mbjac4xab@185.242.93.101:8441',
    'http://tihyjcyk:sr9mbjac4xab@37.35.41.215:8561',
    'http://tihyjcyk:sr9mbjac4xab@37.35.43.48:8906',
    'http://tihyjcyk:sr9mbjac4xab@5.154.254.244:5255',
    'http://tihyjcyk:sr9mbjac4xab@193.151.160.198:8285',
    'http://tihyjcyk:sr9mbjac4xab@5.157.130.1:8005',
    'http://tihyjcyk:sr9mbjac4xab@192.156.217.96:7170',
    'http://tihyjcyk:sr9mbjac4xab@193.23.253.161:7733',
    'http://tihyjcyk:sr9mbjac4xab@45.137.40.128:8681',
    'http://tihyjcyk:sr9mbjac4xab@192.156.217.58:7132',
    'http://tihyjcyk:sr9mbjac4xab@45.131.212.215:6264',
    'http://tihyjcyk:sr9mbjac4xab@45.72.55.37:7074',
    'http://tihyjcyk:sr9mbjac4xab@193.8.215.188:8207',
    'http://tihyjcyk:sr9mbjac4xab@192.153.171.192:6265',
    'http://tihyjcyk:sr9mbjac4xab@193.23.253.152:7724',
    'http://tihyjcyk:sr9mbjac4xab@5.157.130.70:8074',
    'http://tihyjcyk:sr9mbjac4xab@45.92.247.229:6737',
    'http://tihyjcyk:sr9mbjac4xab@45.72.55.80:7117',
    'http://tihyjcyk:sr9mbjac4xab@45.130.60.202:9729',
    'http://tihyjcyk:sr9mbjac4xab@192.153.171.10:6083',
    'http://tihyjcyk:sr9mbjac4xab@193.23.253.52:7624',
    'http://tihyjcyk:sr9mbjac4xab@176.116.231.126:7468',
    'http://tihyjcyk:sr9mbjac4xab@193.23.253.236:7808',
    'http://tihyjcyk:sr9mbjac4xab@45.131.212.76:6125',
    'http://tihyjcyk:sr9mbjac4xab@193.8.215.211:8230',
    'http://tihyjcyk:sr9mbjac4xab@45.137.40.12:8565',
    'http://tihyjcyk:sr9mbjac4xab@193.151.161.60:8403',
    'http://tihyjcyk:sr9mbjac4xab@193.151.161.111:8454',
    'http://tihyjcyk:sr9mbjac4xab@193.151.161.116:8459',
    'http://tihyjcyk:sr9mbjac4xab@5.157.130.189:8193',
    'http://tihyjcyk:sr9mbjac4xab@176.116.231.117:7459',
    'http://tihyjcyk:sr9mbjac4xab@45.131.213.90:7638',
    'http://tihyjcyk:sr9mbjac4xab@45.87.249.101:7679',
    'http://tihyjcyk:sr9mbjac4xab@45.87.249.140:7718',
    'http://tihyjcyk:sr9mbjac4xab@5.154.253.215:8473',
    'http://tihyjcyk:sr9mbjac4xab@192.198.126.10:7053',
    'http://tihyjcyk:sr9mbjac4xab@45.130.60.42:9569',
    'http://tihyjcyk:sr9mbjac4xab@5.157.131.212:8472',
    'http://tihyjcyk:sr9mbjac4xab@45.130.60.105:9632',
    'http://tihyjcyk:sr9mbjac4xab@45.131.212.251:6300',
    'http://tihyjcyk:sr9mbjac4xab@45.131.212.194:6243',
    'http://tihyjcyk:sr9mbjac4xab@45.130.60.76:9603',
    'http://tihyjcyk:sr9mbjac4xab@45.92.247.31:6539',
    'http://tihyjcyk:sr9mbjac4xab@176.116.230.220:7306',
    'http://tihyjcyk:sr9mbjac4xab@193.8.231.204:9210',
    'http://tihyjcyk:sr9mbjac4xab@5.154.253.209:8467',
    'http://tihyjcyk:sr9mbjac4xab@45.92.247.187:6695',
    'http://tihyjcyk:sr9mbjac4xab@45.87.249.235:7813',
    'http://tihyjcyk:sr9mbjac4xab@193.8.231.129:9135',
    'http://tihyjcyk:sr9mbjac4xab@2.56.101.231:8763',
    'http://tihyjcyk:sr9mbjac4xab@45.92.247.176:6684',
    'http://tihyjcyk:sr9mbjac4xab@2.56.101.12:8544',
    'http://tihyjcyk:sr9mbjac4xab@2.56.101.69:8601',
    'http://tihyjcyk:sr9mbjac4xab@195.158.192.228:8805',
    'http://tihyjcyk:sr9mbjac4xab@195.158.192.241:8818',
    'http://tihyjcyk:sr9mbjac4xab@45.92.247.189:6697',
    'http://tihyjcyk:sr9mbjac4xab@85.209.129.154:8694',
    'http://tihyjcyk:sr9mbjac4xab@2.56.101.122:8654',
    'http://tihyjcyk:sr9mbjac4xab@85.209.130.132:7673',
    'http://tihyjcyk:sr9mbjac4xab@193.8.231.21:9027'
]


def error_handle(fun):
    def wrapper(*args):
        try:
            return fun(*args)
        except Exception as e:
            return {"id": args[-1], "msg": str(e)}

    return wrapper


@error_handle
@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(5))
def fetch_data(url, render_way="bs4"):
    ip = random.choice(ip_list)
    proxies = {'http': ip, 'https': ip}
    headers = {
        'user-agent':
        ua.random,
        'accept-language':
        'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5'
    }
    req = requests.get(url, headers=headers, proxies=proxies)
    print(req.status_code)
    if render_way == "bs4":
        soup = BeautifulSoup(req.content, 'html.parser')
        return soup
    elif render_way == "json":
        return json.loads(req.text)


# def start_thread(threads,fun,*args):
#     threads.append(threading.Thread(target = fun, args = (args)))
#     time.sleep(0.05)
#     threads[-1].start()

# def main(fun, fixed_url, id_list, error_log):
#     threads =[]
#     for id in id_list:
#         start_thread(threads,fun,fixed_url, id, error_log)
#     for i in threads:
#         i.join()

if __name__ == "__main__":
    fetch_data("https://www.google.com.tw/")
