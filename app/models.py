from datetime import datetime
from app import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    asset_symbol = db.Column(db.String(20), nullable=False)
    asset_type = db.Column(db.String(10), nullable=False)  # 'crypto' or 'stock'
    condition = db.Column(db.String(2), nullable=False)    # '>', '<', '%' for percentage
    threshold = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_notified = db.Column(db.DateTime, nullable=True)   # For cooldown

    def __repr__(self):
        return f'<Alert {self.asset_symbol} {self.condition} {self.threshold}>'

class PriceLog(db.Model):
    __tablename__ = 'price_logs'

    id = db.Column(db.Integer, primary_key=True)
    asset_symbol = db.Column(db.String(20), nullable=False)
    asset_type = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

class NotificationLog(db.Model):
    __tablename__ = 'notification_logs'

    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    alert = db.relationship('Alert', backref='notifications')
