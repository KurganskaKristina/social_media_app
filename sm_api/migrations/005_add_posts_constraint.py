from yoyo import step

__depends__ = {"001_init_users_table", "002_init_posts_table"}

steps = [
    step(
        "ALTER TABLE posts ADD CONSTRAINT posts_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;",
        "ALTER TABLE posts DROP CONSTRAINT posts_users_fk"),
]
