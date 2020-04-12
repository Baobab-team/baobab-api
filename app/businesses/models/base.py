from datetime import datetime

from app import db


class BaseModel(db.Model):
    __abstract__ = True


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def delete(self):
        self.deleted_at = datetime.utcnow()
