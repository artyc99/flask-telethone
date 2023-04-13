from dataclasses import dataclass

from flask_login import UserMixin


@dataclass
class Admin(UserMixin):

    id: int

    login: str
    password: str
