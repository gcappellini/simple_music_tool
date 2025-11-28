-- ============================
--  ARTIST
-- ============================
CREATE TABLE IF NOT EXISTS artist (
    artist_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    instagram_id    TEXT,
    spotify_id      TEXT,
    youtube_id      TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================
--  TRACK
-- ============================
CREATE TABLE IF NOT EXISTS track (
    track_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id       INTEGER NOT NULL,
    title           TEXT NOT NULL,
    spotify_id      TEXT,
    youtube_id      TEXT,
    release_date    DATE,
    duration_ms     INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (artist_id)
        REFERENCES artist(artist_id)
        ON DELETE CASCADE
);

-- ============================
--  TRACK STATS (daily stats per platform)
-- ============================
CREATE TABLE IF NOT EXISTS track_stats (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id        INTEGER NOT NULL,
    platform        TEXT NOT NULL,   -- 'spotify', 'youtube', etc.
    date            DATE NOT NULL,   -- normalized day
    value_1         INTEGER,         -- streams / views
    value_2         INTEGER,         -- likes / watch time / saves
    value_3         INTEGER,         -- comments / shares
    growth_rate     REAL,
    momentum_score  REAL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
        ON DELETE CASCADE,

    UNIQUE (track_id, platform, date)
);

-- Useful index
CREATE INDEX IF NOT EXISTS idx_track_stats_track_date
    ON track_stats(track_id, date);

-- ============================
--  FAN ACTIVITY (hourly)
-- ============================
CREATE TABLE IF NOT EXISTS fan_activity (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id       INTEGER NOT NULL,
    platform        TEXT NOT NULL,    -- 'instagram', 'youtube'
    date            DATE NOT NULL,    -- normalized day
    hour            INTEGER NOT NULL, -- 0–23
    activity_score  REAL NOT NULL,    -- normalized engagement
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (artist_id)
        REFERENCES artist(artist_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_fan_activity_artist_date_hour
    ON fan_activity(artist_id, date, hour);

-- ============================
--  AUDIO FEATURES + EMBEDDINGS
-- ============================
CREATE TABLE IF NOT EXISTS audio_features (
    track_id        INTEGER PRIMARY KEY,
    danceability    REAL,
    energy          REAL,
    valence         REAL,
    tempo           REAL,
    acousticness    REAL,
    instrumentalness REAL,
    liveness        REAL,
    speechiness     REAL,
    embedding_path  TEXT,  -- path to local .npy embedding
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
        ON DELETE CASCADE
);

-- ============================
--  VISUAL MEDIA (images + embeddings)
-- ============================
CREATE TABLE IF NOT EXISTS visual_media (
    image_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id       INTEGER NOT NULL,
    platform        TEXT NOT NULL,     -- 'instagram', 'youtube'
    media_url       TEXT,
    local_path      TEXT,              -- locally saved image
    embedding_path  TEXT,              -- .npy embedding
    cluster_id      INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (artist_id)
        REFERENCES artist(artist_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_visual_media_artist
    ON visual_media(artist_id);

-- ============================
--  SIMILARITY CACHE
-- ============================
CREATE TABLE IF NOT EXISTS similarity_cache (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type     TEXT NOT NULL,    -- 'track_audio' or 'visual'
    source_id       INTEGER NOT NULL, -- track_id or image_id
    compared_id     INTEGER NOT NULL, -- track_id or image_id
    score           REAL NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_similarity_cache_source
    ON similarity_cache(source_type, source_id);

-- ============================
--  RELEASE RECOMMENDATIONS
-- ============================
CREATE TABLE IF NOT EXISTS release_recommendation (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id       INTEGER NOT NULL,
    track_id        INTEGER,
    date_generated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    best_day        TEXT,        -- 'Thursday'
    best_hour       TEXT,        -- '18:00-21:00'
    momentum_status TEXT,        -- 'rising', 'stable', 'cooling'
    notes           TEXT,

    FOREIGN KEY (artist_id)
        REFERENCES artist(artist_id)
        ON DELETE CASCADE,

    FOREIGN KEY (track_id)
        REFERENCES track(track_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recommendation_artist
    ON release_recommendation(artist_id);