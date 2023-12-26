from datetime import datetime

import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase


class BaseEntity(DeclarativeBase):
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
