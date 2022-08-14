from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS likes (
            id SERIAL PRIMARY KEY,
            user_id INT,
            post_id INT,
            creation_date TIMESTAMP,
            UNIQUE (user_id, post_id)
        );""",
         "DROP TABLE likes"
         )
]
