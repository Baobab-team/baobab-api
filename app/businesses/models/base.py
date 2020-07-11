from datetime import datetime
from sqlalchemy import Column,DateTime

from app.database import Base


class BaseModel(Base):
    __abstract__ = True


class TimestampMixin(object):
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)

    def is_deleted(self):
        if self.deleted_at is None:
            return True
        return False

    def delete(self):
        self.deleted_at = datetime.utcnow()
