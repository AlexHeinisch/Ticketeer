CREATE TABLE IF NOT EXISTS users(
    username varchar(20) PRIMARY KEY,
    password_hash varchar(255) NOT NULL,
    email varchar(40) NOT NULL,
    icon_id NUMERIC(8),
    role varchar(20) NOT NULL
)