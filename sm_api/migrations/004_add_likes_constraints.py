from yoyo import step

__depends__ = {"001_init_users_table", "002_init_posts_table", "003_init_likes_table"}

steps = [
    step(
        "ALTER TABLE likes ADD CONSTRAINT likes_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;",
        "ALTER TABLE likes DROP CONSTRAINT likes_users_fk"),
    step(
        "ALTER TABLE likes ADD CONSTRAINT likes_posts_fk FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE;",
        "ALTER TABLE likes DROP CONSTRAINT likes_posts_fk"),
]
