from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from peewee import AutoField, TextField, DateTimeField, IntegerField, IntegrityError, DataError

from sm_api.models.base import BaseModel, db


@dataclass(frozen=True)
class PostData:
    id: int
    title: str
    text: str
    user_id: int
    creation_date: datetime


class PostsModel(BaseModel):
    class Meta:
        table_name = "posts"

    id = AutoField()
    title = TextField()
    text = TextField()
    user_id = IntegerField()
    creation_date = DateTimeField()

    @classmethod
    def length(cls) -> int:
        return cls.select().count()

    @classmethod
    @db.atomic()
    def get_post(cls, post_id: int) -> Optional[dict]:
        if post_id is None:
            return
        post = cls.select(cls.id).where(cls.id == post_id).first()
        return post

    @classmethod
    @db.atomic()
    def get_posts(cls, user_id: int = None):
        res_data = {
            "posts": [],
            "posts_amount": 0
        }
        if user_id is None:
            data = cls.select().dicts().order_by(cls.id.desc())
        else:
            data = cls.select().where(cls.user_id == user_id).dicts().order_by(cls.id.desc())

        res_data["posts"] = [item for item in data]
        res_data["posts_amount"] = len(res_data["posts"])

        return res_data

    @classmethod
    @db.atomic()
    def add_post(cls, title: str, text: str, user_id: int) -> int:
        try:
            last_row_id = cls.insert(
                title=title,
                text=text,
                user_id=user_id,
                creation_date=datetime.now()
            ).execute()
            return last_row_id
        except DataError:
            pass
        except IntegrityError:
            pass

    @classmethod
    @db.atomic()
    def delete_post(cls, post_id: int):
        data = cls.select().where(cls.id == post_id).first()

        if data is None:
            return False

        cls.get(cls.id == post_id).delete_instance()

        return True
