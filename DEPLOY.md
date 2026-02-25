# 🚀 Tamamen Ücretsiz Deploy

## Platform: Vercel + Render + Supabase

---

### 1. Supabase (PostgreSQL - ÜCRETSİZ)

1. https://supabase.com adresine git → GitHub ile giriş
2. "New Project" → İsim ver (örn: localcateringos)
3. Şifre belirle → Project oluştur
4. **Settings → Database** dan connection string'i al:
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

---

### 2. Backend → Render (ÜCRETSİZ)

1. https://render.com adresine git → GitHub ile giriş
2. "New Web Service"
3. Bu GitHub reposu seçilir
4. Ayarlar:
   - **Name**: localcateringos-backend
   - **Build Command**: (boş - Dockerfile kullanılacak)
   - **Start Command**: `gunicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables** ekle:
   ```
   DATABASE_URL = postgresql://postgres:[ŞİFRE]@db.[REF].supabase.co:5432/postgres
   SECRET_KEY = random-string-secret-key-12345
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 480
   ```
6. Create Web Service

---

### 3. Frontend → Vercel (ÜCRETSİZ)

1. https://vercel.com adresine git → GitHub ile giriş
2. "New Project" → Bu repo seçilir
3. Ayarlar:
   - **Framework Preset**: Vite
   - **Build Command**: npm run build
   - **Output Directory**: frontend/dist
4. **Environment Variables**:
   ```
   VITE_API_URL = https://localcateringos-backend.onrender.com
   ```
5. Deploy!

---

### 🔑 İlk Giriş

| Rol | E-posta | Şifre |
|-----|---------|-------|
| Chief | admin@catering.com | admin123 |
| Pazarlama | pazarlama@catering.com | pazarlama123 |

---

### ⚠️ Önemli Not

1. Supabase'de yukarıdaki SQL'i çalıştır (Schema kısmında)
2. Backend ilk çalıştığında veritabanı tabloları otomatik oluşur
3. Kullanıcıları backend /docs üzerinden oluştur veya Supabase'den INSERT yap

---

## 💰 Ücretsiz Limitler

| Servis | Limit |
|--------|-------|
| Supabase DB | 500MB |
| Render | 750 saat/ay |
| Vercel | Sınırsız (frontend) |
