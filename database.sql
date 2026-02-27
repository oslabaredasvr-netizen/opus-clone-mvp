-- Extensão para geração de IDs únicos Universais (UUID)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Usuários (Integrado de forma Custom ao Supabase Auth)
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    credits INT DEFAULT 100, -- Sistema de balanceamento para o SaaS
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 2. Registro dos Vídeos Originais Processados
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    original_url TEXT, -- URL de onde foi puxado (ex: storage ou youtube)
    title VARCHAR(255),
    status VARCHAR(50) DEFAULT 'processing', -- processing, done, error
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 3. Clipes Gerados (Resultados do Módulo 1)
CREATE TABLE generated_clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    title VARCHAR(255),
    start_time FLOAT,  -- Marcação exata de início
    end_time FLOAT,    -- Marcação exata de fim
    clip_url TEXT,     -- URL no Supabase Storage do corte gerado
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 4. Artes Geradas (Resultados do Módulo 2)
CREATE TABLE generated_arts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(255),
    headline TEXT,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
