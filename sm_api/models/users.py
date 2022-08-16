from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass

from peewee import AutoField, TextField, DateTimeField, IntegrityError, DataError

from sm_api.models.base import BaseModel, db


@dataclass(frozen=True)
class UserData:
    id: int
    first_name: str
    last_name: str
    login: str
    password: str
    last_login: datetime
    last_request: datetime


class UsersModel(BaseModel):
    class Meta:
        table_name = "users"

    id = AutoField()
    first_name = TextField()
    last_name = TextField()
    login = TextField()
    password = TextField()
    last_login = DateTimeField()
    last_request = DateTimeField()

    @classmethod
    def length(cls) -> int:
        return cls.select().count()

    @classmethod
    @db.atomic()
    def get_user(cls, login: str = None, user_id: int = None) -> Optional[dict]:
        if login is None and user_id is None:
            return
        query = cls.select().where(cls.login == login) if user_id is None else cls.select().where(cls.user_id == user_id)
        return query.dicts().first()

    @classmethod
    @db.atomic()
    def get_registered_user(cls, login, password) -> Optional[dict]:
        user = cls.select(cls.id).where(cls.login == login, cls.password == password).dicts().first()
        return user

    @classmethod
    @db.atomic()
    def get_users(cls, amount: int = None) -> Optional[List[dict]]:
        if amount is None:
            amount = cls.length()
        data = cls.select().dicts().order_by(cls.id.desc()).limit(int(amount))
        res_data = [item for item in data]
        return res_data

    @classmethod
    @db.atomic()
    def get_user_activity(cls, user_id: int) -> Optional[dict]:
        data = cls.select(cls.id, cls.last_login, cls.last_request).where(cls.id == user_id).dicts().first()
        return data

    @classmethod
    @db.atomic()
    def add_user(cls, first_name: str, last_name: str, login: str, password: str) -> int:
        try:
            last_row_id = cls.insert(
                first_name=first_name,
                last_name=last_name,
                login=login,
                password=password,
                last_login=None,
                last_request=None
            ).execute()
            return last_row_id
        except DataError:
            pass
        except IntegrityError:
            pass

    @classmethod
    @db.atomic()
    def modify_user(cls, user_id: int, **kwargs) -> bool:
        try:
            data_query = cls.select().where(cls.id == user_id)
            data = data_query.first()
            data_dict = data_query.dicts().first()

            if data is None:
                return False

            for key in data_dict.keys():
                if key in kwargs and kwargs[key] is not None:
                    data_dict[key] = kwargs[key]

            data.first_name = data_dict["first_name"]
            data.last_name = data_dict["last_name"]
            data.login = data_dict["login"]
            data.password = data_dict["password"]
            data.last_login = data_dict["last_login"]
            data.last_request = data_dict["last_request"]
            data.save()
            return True
        except DataError as e:
            pass
        except IntegrityError as e:
            pass

        return False

    @classmethod
    @db.atomic()
    def delete_user(cls, user_id: int):
        data = cls.select().where(cls.id == user_id).first()

        if data is None:
            return False

        cls.get(cls.id == user_id).delete_instance()

        return True
