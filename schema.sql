CREATE TABLE IF NOT EXISTS lists (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT TIMESTAMP 'now' NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    list_id BIGINT NOT NULL,
    movie_id BIGINT NOT NULL,
    title TEXT NOT NULL,
    overview TEXT,
    poster_path TEXT,
    backdrop_path TEXT,
    release_date DATE,
    rating SMALLINT,
    suggested_by BIGINT NOT NULL,
    approved BOOLEAN DEFAULT FALSE NOT NULL,
    watched BOOLEAN DEFAULT FALSE NOT NULL,
    watched_at TIMESTAMP,
    UNIQUE (list_id, movie_id)
);

CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    item_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    vote BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT TIMESTAMP 'now' NOT NULL,
    UNIQUE (item_id, user_id)
);