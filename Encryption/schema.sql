CREATE TABLE IF NOT EXISTS keys (
    username TEXT PRIMARY KEY,
    public_key INTEGER NOT NULL,
    imagepath TEXT NOT NULL
);
