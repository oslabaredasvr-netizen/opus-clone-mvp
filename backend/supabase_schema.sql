-- SQL Migration Script para o Supabase
-- Cole e execute isso no "SQL Editor" do painel do Supabase

CREATE TABLE video_jobs (
    id TEXT PRIMARY KEY,
    video_url TEXT NOT NULL,
    status TEXT DEFAULT 'processing',
    error_message TEXT
);

CREATE TABLE generated_clips (
    id SERIAL PRIMARY KEY,
    job_id TEXT REFERENCES video_jobs(id) ON DELETE CASCADE,
    title TEXT,
    start_time_str TEXT,
    end_time_str TEXT,
    clip_path TEXT
);

-- Habilitar RLS (Row Level Security) para acesso público (APENAS PARA O MVP)
ALTER TABLE video_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_clips ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow anonymous read access on video_jobs" ON video_jobs FOR SELECT USING (true);
CREATE POLICY "Allow anonymous insert access on video_jobs" ON video_jobs FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anonymous update access on video_jobs" ON video_jobs FOR UPDATE USING (true);

CREATE POLICY "Allow anonymous read access on generated_clips" ON generated_clips FOR SELECT USING (true);
CREATE POLICY "Allow anonymous insert access on generated_clips" ON generated_clips FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anonymous update access on generated_clips" ON generated_clips FOR UPDATE USING (true);
