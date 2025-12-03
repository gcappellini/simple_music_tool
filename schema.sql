-- ===================================================
--  PROFILE DAILY STATS
--  (follower count, total reach, etc.)
-- ===================================================
CREATE TABLE IF NOT EXISTS profile_stats (
    date            DATE PRIMARY KEY,
    platform        TEXT NOT NULL,      -- 'instagram' or 'youtube'
    followers       INTEGER,            -- total followers/subscribers count
    total_views     INTEGER,            -- total views across posts for that day (optional)
    total_engagement INTEGER,           -- sum of likes + comments + shares for the day (optional)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
--  POST / VIDEO METADATA + DAILY STATS
-- ===================================================
CREATE TABLE IF NOT EXISTS post (
    post_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    platform        TEXT NOT NULL,       -- 'instagram' or 'youtube'
    external_id     TEXT UNIQUE NOT NULL,  -- the IG post ID or YT video ID
    created_at_post DATETIME NOT NULL,   -- when you posted
    caption         TEXT,                -- optional
    description     TEXT,                -- optional (for YT)
    uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS post_stats (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id         INTEGER NOT NULL,
    date            DATE NOT NULL,       -- stats snapshot date
    views           INTEGER,             -- total views / reach / impressions
    likes           INTEGER,
    comments        INTEGER,
    shares          INTEGER,            -- share/repost count (if available)
    retention       REAL,               -- if you can capture retention/watch-time ratio (optional)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    UNIQUE (post_id, date)
);

-- ===================================================
--  FAN / AUDIENCE ACTIVITY (hourly) — for timing engine
--  (when followers are active / audience online)
-- ===================================================
CREATE TABLE IF NOT EXISTS activity_hourly (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    platform        TEXT NOT NULL,       -- 'instagram' or 'youtube'
    date            DATE NOT NULL,
    hour            INTEGER NOT NULL,    -- 0–23
    activity_score  REAL NOT NULL,       -- normalized activity (e.g. number of online followers, views per hour, etc.)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, date, hour)
);

-- ===================================================
--  POSTING RECOMMENDATIONS (output of your timing / growth engine)
-- ===================================================
CREATE TABLE IF NOT EXISTS posting_recommendation (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date_generated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    platform        TEXT NOT NULL,    -- 'instagram' or 'youtube'
    recommended_date DATE,            -- e.g. '2025-12-09'
    recommended_hour INTEGER,         -- e.g. 20  (representing 20:00)
    reason          TEXT              -- explanation / notes
);