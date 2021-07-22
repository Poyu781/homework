from email.mime.multipart import MIMEMultipart
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import GMAIL_PASSWORD
from datetime import datetime

def send_email(title,text):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = title  #郵件標題
    content["from"] = "v3708599@gmail.com"  #寄件者
    content["to"] = "poyu850122@gmail.com" #收件者
    content.attach(MIMEText(text))  #郵件內容
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("v3708599@gmail.com", GMAIL_PASSWORD)  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
        except Exception as e:
            print("Error message: ", e)
if __name__ == "__main__":
    send_email("3","3")