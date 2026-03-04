# TEKNOFEST 2025 - Teknik Yeterlilik Formu (TYF)

## 1. Takım ve Proje Bilgileri
- **Takım Adı:** SKYGUARD
- **Proje Adı:** Otonom Lojistik Robotu (AMR)
- **Kategori:** İleri Seviye

## 2. Problem Tanımı
İmalat sanayinde malzeme taşıma süreçlerinin otonomlaştırılması, insan hatasını azaltmak ve verimliliği artırmak için kritiktir. Mevcut sistemler genellikle esneklikten yoksundur.

## 3. Çözüm Önerisi
Doğal navigasyon (LiDAR tabanlı), QR kod destekli konum doğrulama ve gerçek zamanlı merkezi izleme arayüzüne sahip AMR sistemi.

## 4. Teknik Özellikler
- **Navigasyon:** SLAM & Doğal Navigasyon
- **Haberleşme:** Wi-Fi / WebSocket
- **Güvenlik:** Acil Durdurma Butonu + Kauçuk Kenar Sensörü
- **İzleme:** Web tabanlı GUI

## 5. Risk Analizi ve Önlemler
- **Risk:** Çizgi takibi kaybı (Temel seviye)
- **Önlem:** QR kod doğrulama noktaları ile re-lokalizasyon.
