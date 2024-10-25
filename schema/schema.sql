\c vinylvault

DROP TABLE IF EXISTS access_tokens;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS album CASCADE;
DROP TABLE IF EXISTS artist CASCADE;
DROP TABLE IF EXISTS artist_genre_assignment;
DROP TABLE IF EXISTS album_genre_assignment;

CREATE TABLE access_tokens(
    access_token_id INT GENERATED ALWAYS AS IDENTITY,
    client_id VARCHAR NOT NULL,
    access_token TEXT UNIQUE NOT NULL,
    client_secret VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (access_token_id),
    CHECK (created_at <= NOW())
);

CREATE TABLE artist(
    artist_id INT GENERATED ALWAYS AS IDENTITY,
    spotify_artist_id VARCHAR(50) UNIQUE,
    artist_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (artist_id)
);

CREATE TABLE genre(
    genre_id INT GENERATED ALWAYS AS IDENTITY,
    genre_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (genre_id)
);

CREATE TABLE album(
    album_id INT GENERATED ALWAYS AS IDENTITY,
    artist_id INT NOT NULL,
    spotify_album_id VARCHAR(50) UNIQUE,
    album_type VARCHAR(50),
    album_name VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    num_tracks SMALLINT NOT NULL,
    runtime_seconds SMALLINT NOT NULL,
    album_art_url TEXT,
    PRIMARY KEY (album_id),
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

CREATE TABLE album_genre_assignment(
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    album_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE,
    UNIQUE (album_id, genre_id)
);

CREATE TABLE artist_genre_assignment(
    assignment_id INT GENERATED ALWAYS AS IDENTITY,
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE,
    UNIQUE (artist_id, genre_id)
);

CREATE INDEX idx_spotify_artist_id ON artist(spotify_artist_id, artist_name);
CREATE INDEX idx_spotify_album_id ON album(spotify_album_id, album_name);