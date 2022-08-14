from typing import List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from peewee import AutoField, DateTimeField, IntegerField, IntegrityError, DataError

from sm_api.models.base import BaseModel, db


@dataclass(frozen=True)
class LikeData:
    id: int
    user_id: int
    post_id: int
    creation_date: datetime


class LikesModel(BaseModel):
    class Meta:
        table_name = "likes"

    id = AutoField()
    user_id = IntegerField()
    post_id = IntegerField()
    creation_date = DateTimeField()

    @classmethod
    def length(cls) -> int:
        return cls.select().count()

    @classmethod
    def get_likes(cls, user_id: int = None):
        res_data = {
            "likes": [],
            "likes_amount": 0
        }
        if user_id is None:
            data = cls.select().dicts().order_by(cls.id.desc())
        else:
            data = cls.select().where(cls.user_id == user_id).dicts().order_by(cls.id.desc())

        res_data["likes"] = [item for item in data]
        res_data["likes_amount"] = len(res_data["likes"])

        return res_data

    @classmethod
    def get_likes_for_period(cls, date_from: datetime, date_to: datetime):
        dates = [date_from + timedelta(days=x) for x in range((date_to - date_from).days)]
        res_data = []

        for date in dates:
            likes_amount = cls.select().where(cls.creation_date == date).count()
            data = {
                "day": date.strftime("%m/%d/%Y"),
                "likes": likes_amount
            }
            res_data.append(data)

        return res_data

    @classmethod
    @db.atomic()
    def add_like(cls, user_id: int, post_id: int) -> int:
        try:
            last_row_id = cls.insert(
                user_id=user_id,
                post_id=post_id,
                creation_date=datetime.now()
            ).execute()
            return last_row_id
        except DataError:
            pass
        except IntegrityError:
            pass

    @classmethod
    @db.atomic()
    def delete_like(cls, user_id: int, post_id: int):
        data = cls.select().where(cls.user_id == user_id, cls.post_id == post_id).first()

        if data is None:
            return False

        cls.get(cls.user_id == user_id, cls.post_id == post_id).delete_instance()

        return True
