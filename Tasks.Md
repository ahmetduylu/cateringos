# LocalCateringOS - Proje Yol Haritası

---

## FAZ 1: Veritabanı Mimarisi ve Altyapı Kurulumu

### Task 1.1: Veritabanı Seçimi ve Kurulumu
- [x] PostgreSQL — Docker container olarak çalıştırılacak
- [x] `localcateringos` veritabanı (docker-compose ile otomatik oluşturulacak)

### Task 1.2: Tabloların (Schema) Tasarlanması ve Oluşturulması
- [x] **users** tablosu: `id`, `ad`, `email`, `password_hash`, `rol` (marketing | chief)
- [x] **leads** tablosu: `id`, `isletme_adi`, `telefon`, `adres`, `harita_linki`, `eklenme_tarihi`, `assigned_user_id`, `status`
- [x] **lead_logs** tablosu: `id`, `lead_id`, `user_id`, `islem_turu`, `aciklama`, `tarih`

### Task 1.3: Satış Aşamalarının (Pipeline) Belirlenmesi
- [x] `havuzda` | `aranmadi_ulasma` | `gorusuldu_olumlu` | `teklif_iletildi` | `kazanildi` | `ilgilenmiyor`

---

## FAZ 2: Backend

**Stack:** Python 3.12 + FastAPI + SQLAlchemy + Alembic + JWT

### Task 2.1: Auth
- [x] `POST /auth/login` — JWT tabanlı giriş
- [x] `GET /auth/me` — Mevcut kullanıcı
- [x] Rol tabanlı erişim kontrolü

### Task 2.2: Havuz ve Atama
- [x] `GET /leads/pool`
- [x] `POST /leads/assign` — SELECT FOR UPDATE (çakışma korumalı)

### Task 2.3: Portföy
- [x] `GET /leads/my-leads`
- [x] `PUT /leads/{id}/status`
- [x] `POST /leads/{id}/note`

### Task 2.4: Raporlama
- [x] `GET /reports/team`
- [x] `GET /reports/pool-stats`

---

## FAZ 3: Apify Entegrasyonu
- [x] `POST /apify/webhook` — Veri karşılama endpoint'i
- [x] Telefon bazlı deduplication
- [ ] Apify hesabı açılması (manuel)
- [ ] Google Maps Scraper aktörü ayarı (manuel)

---

## FAZ 4: Frontend

**Stack:** React 18 + Vite + Tailwind CSS + Zustand + Axios

- [x] Login ekranı
- [x] Role-based sidebar
- [x] Havuz Ekranı (filtrelenebilir tablo + Bana Ata)
- [x] Portföyüm Ekranı (status dropdown + not modal)
- [x] Şef Dashboard (istatistik kartlar + personel tablosu)

---

## FAZ 5: Deployment

- [x] Docker Compose ile tek komut deployment
- [ ] Domain / IP erişim konfigürasyonu (manuel)

---

## Kurulum Adımları (Sırayla)

1. `C:\Users\Administrator\Downloads\Git-2.53.0-64-bit.exe` — Git'i kur
2. `C:\Users\Administrator\Downloads\Docker Desktop Installer.exe` — Docker Desktop'u kur, sistemi yeniden başlat
3. Bu dizinde terminali aç: `C:\Users\Administrator\Desktop\Projects\LocalCateringOS`
4. `docker-compose up --build -d` komutunu çalıştır
5. Tarayıcıdan `http://localhost:3000` adresine git

## Servis Portları

| Servis | Port | URL |
|--------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| PostgreSQL | 5432 | (dahili) |

*Oluşturulma tarihi: 25 Şubat 2026*
