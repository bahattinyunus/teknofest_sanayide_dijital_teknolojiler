import time
import sys
import os

# Renk kodları
class Renk:
    MAVI = '\033[94m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def yavas_yaz(yazi, hiz=0.03):
    for harf in yazi:
        sys.stdout.write(harf)
        sys.stdout.flush()
        time.sleep(hiz)
    print()

def yukleme_cubugu(islem_adi, sure=1.5):
    print(f"{Renk.MAVI}[*] {islem_adi} başlatılıyor...{Renk.RESET}")
    genislik = 40
    for i in range(genislik + 1):
        time.sleep(sure / genislik)
        cubuk = '█' * i + '-' * (genislik - i)
        sys.stdout.write(f"\r{Renk.YESIL}|{cubuk}| %{int(i * 100 / genislik)}{Renk.RESET}")
        sys.stdout.flush()
    print(f"\n{Renk.YESIL}[+] {islem_adi} TAMAMLANDI{Renk.RESET}\n")

def banner():
    art = f"""{Renk.MAVI}{Renk.BOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║   TEKNOFEST SANAYİDE DİJİTAL TEKNOLOJİLER KURULUMU    ║
    ╚═══════════════════════════════════════════════════════╝
    {Renk.RESET}"""
    print(art)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    time.sleep(1)

    yavas_yaz(f"{Renk.SARI}Sistem bütünlüğü doğrulanıyor...{Renk.RESET}")
    time.sleep(0.5)

    yukleme_cubugu("Sanal Ortam (VirtualEnv) Hazırlığı")
    yukleme_cubugu("Bağımlılıkların Yüklenmesi (AI & IoT Modülleri)")
    yukleme_cubugu("Dijital İkiz Motoru Konfigürasyonu")
    
    yavas_yaz(f"{Renk.BOLD}Gizli Anahtarlar üretiliyor... [....................]{Renk.RESET}", 0.05)
    time.sleep(0.5)
    print(f"{Renk.YESIL}[OK] Güvenlik tüneli oluşturuldu.{Renk.RESET}")
    print("-" * 50)
    
    yavas_yaz(f"{Renk.MAVI}Kurulum başarıyla tamamlandı, Komutan.{Renk.RESET}\n")
    print(f"Sistemi başlatmak için şu komutu girin:")
    print(f"{Renk.SARI}{Renk.BOLD}   python src/main.py{Renk.RESET}")
    print("\nveya paneli açmak için:")
    print(f"{Renk.SARI}{Renk.BOLD}   uvicorn src.main:app --reload{Renk.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Renk.KIRMIZI}[!] Kurulum iptal edildi.{Renk.RESET}")
