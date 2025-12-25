# Hafif siklet Python imajı kullan
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kaynak kodunu kopyala
COPY src/ ./src/

# Yetkisiz kullanıcı oluştur (Güvenlik standardı)
RUN useradd -m teknofest
USER teknofest

# Uygulamayı başlat
CMD ["python", "src/main.py"]
