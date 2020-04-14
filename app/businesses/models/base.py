from datetime import datetime

from app import db


class BaseModel(db.Model):
    __abstract__ = True


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(self, **kwargs):
        super(TimestampMixin,self).__init__(**kwargs)
        self.deactivated_at = None

    def is_active(self):
        return self.deactivated_at is None

    def activate(self):
        self.deactivated_at = None

    def deactivate(self):
        self.deactivated_at = datetime.utcnow()
