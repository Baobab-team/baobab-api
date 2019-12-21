from datetime import datetime

from api.app import db


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    activated = db.Column(db.Boolean, default=True,nullable=False)

    def deactivate(self):
        self.activated = False

    def activate(self):
        self.activated = True
