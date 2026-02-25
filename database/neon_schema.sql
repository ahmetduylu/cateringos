-- Neon Database Schema

-- Users tablosu
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    ad VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('marketing', 'chief')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Leads tablosu
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    isletme_adi VARCHAR(255) NOT NULL,
    telefon VARCHAR(50),
    adres TEXT,
    harita_linki TEXT,
    eklenme_tarihi TIMESTAMPTZ DEFAULT NOW(),
    assigned_user_id INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'havuzda' CHECK (status IN ('havuzda', 'aranmadi_ulasma', 'gorusuldu_olumlu', 'teklif_iletildi', 'kazanildi', 'ilgilenmiyor'))
);

-- Lead logs tablosu
CREATE TABLE lead_logs (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    islem_turu VARCHAR(50) NOT NULL,
    aciklama TEXT,
    tarih TIMESTAMPTZ DEFAULT NOW()
);

-- İndeksler
CREATE INDEX idx_leads_assigned_user_id ON leads(assigned_user_id);
CREATE INDEX idx_leads_telefon ON leads(telefon);
CREATE INDEX idx_lead_logs_lead_id ON lead_logs(lead_id);

-- İlk kullanıcılar (şifre: admin123, pazarlama123)
INSERT INTO users (ad, email, password_hash, rol) VALUES 
('Ahmet Yönetici', 'admin@catering.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY1K1e1.JWS', 'chief'),
('Ayşe Pazarlama', 'pazarlama@catering.com', '$2b$12$EqKcp1WFKVQIShe7LX5o5OvZ6iKXQJYhL6YVjuQyP5pMqCIGZMQWy', 'marketing');
