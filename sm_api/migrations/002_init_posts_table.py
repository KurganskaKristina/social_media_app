from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT,
            text TEXT,
            user_id INT,
            creation_date TIMESTAMP
        );""",
         "DROP TABLE posts"
         )
]
