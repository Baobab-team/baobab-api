from datetime import datetime

from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TimestampMixin(object):
    created = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
