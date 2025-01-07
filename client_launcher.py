# client_launcher.py
import os
import subprocess
import requests
import platform
import hashlib
import getpass
import time


def get_machine_signature():
    info = (
            platform.system() +
            platform.node() +
            platform.machine() +
            platform.processor() +
            getpass.getuser()
    )
    return hashlib.sha256(info.encode()).hexdigest()


def verify_license(license_key):
    """
    Flask sunucusuna POST isteği gönderip lisans doğrulaması yapar.
    Dönüş: JSON (status, message)
    """
    url = "http://127.0.0.1:5000/verify"  # Sunucunuz başka IP/host+port ise burayı değiştirin
    payload = {
        "license_key": license_key,
        "machine_signature": get_machine_signature()
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


def main():
    # 1) CMD ekranında kullanıcıya lisans kodunu soralım
    print("******************************")
    print("    Lisans Doğrulama Ekranı   ")
    print("******************************")
    license_key = input("Lisans kodunu giriniz: ")

    # 2) Sunucuya isteği gönderelim
    result = verify_license(license_key)

    # 3) Gelen cevaba göre karar verelim
    if result["status"] == "success":
        # Lisans geçerli
        print("Lisans geçerli. Süreç:", result["message"])
        # (Opsiyonel) Kullanıcıya lisansın bitiş tarihini, kalan günlerini veya benzeri bilgileri gösterebilirsiniz.

        # Kullanıcı ENTER'a basınca CMD ekranı kapansın ve program açılsın
        input("Devam etmek için ENTER tuşuna basın...")

        # 4) Şimdi asıl programı (my_program.py) çalıştıralım:
        #    - Seçenek A: Aynı konsol penceresinde çalıştırmak:
        os.system("main.exe")

        #    - Seçenek B: Yeni bir konsol penceresi açmak isterseniz:
        # subprocess.Popen(["python", "my_program.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

    else:
        # Lisans geçersiz
        print("Hata: ", result["message"])
        print("Lisans doğrulaması başarısız. Program kapatılıyor...")
        time.sleep(3)  # 3 saniye bekleyip kapanabilir
        # Ardından çıkış
        return


if __name__ == "__main__":
    main()
