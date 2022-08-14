from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            login TEXT UNIQUE,
            password TEXT,
            last_login TIMESTAMP,
            last_request TIMESTAMP
        );""",
         "DROP TABLE users"
         )
]
