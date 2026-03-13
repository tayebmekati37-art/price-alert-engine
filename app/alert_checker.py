from datetime import datetime
from app import db
from app.models import Alert, PriceLog, NotificationLog
from app.price_fetcher import fetch_price
from app.notifier import send_alert_email
import logging

logger = logging.getLogger(__name__)

def check_alerts(app):
    with app.app_context():
        alerts = Alert.query.filter_by(active=True).all()
        logger.info(f"Checking {len(alerts)} alerts")

        for alert in alerts:
            try:
                price = fetch_price(alert.asset_type, alert.asset_symbol)
                if price is None:
                    logger.warning(f"Could not fetch price for {alert.asset_symbol} ({alert.asset_type})")
                    continue

                price_log = PriceLog(
                    asset_symbol=alert.asset_symbol,
                    asset_type=alert.asset_type,
                    price=price
                )
                db.session.add(price_log)

                triggered = False
                if alert.condition == '>':
                    triggered = price > alert.threshold
                elif alert.condition == '<':
                    triggered = price < alert.threshold
                elif alert.condition == '%':
                    last_log = PriceLog.query.filter_by(
                        asset_symbol=alert.asset_symbol,
                        asset_type=alert.asset_type
                    ).order_by(PriceLog.fetched_at.desc()).offset(1).first()
                    if last_log and last_log.price > 0:
                        change_pct = ((price - last_log.price) / last_log.price) * 100
                        if alert.threshold > 0:
                            triggered = change_pct > alert.threshold
                        else:
                            triggered = change_pct < alert.threshold
                    else:
                        triggered = False
                else:
                    logger.error(f"Unknown condition {alert.condition} for alert {alert.id}")
                    continue

                if triggered:
                    cooldown = app.config['NOTIFICATION_COOLDOWN']
                    if alert.last_notified and (datetime.utcnow() - alert.last_notified).total_seconds() < cooldown:
                        logger.info(f"Alert {alert.id} triggered but in cooldown")
                        continue

                    subject = f"Price Alert Triggered: {alert.asset_symbol}"
                    body = f"""
Your price alert for {alert.asset_symbol} ({alert.asset_type}) has been triggered.

Condition: {alert.condition} {alert.threshold}
Current price: ${price:.2f}

Alert details:
- Symbol: {alert.asset_symbol}
- Type: {alert.asset_type}
- Threshold: {alert.condition} {alert.threshold}
- Current price: ${price:.2f}

Thank you for using PriceAlertEngine.
                    """
                    if send_alert_email(alert.email, subject, body, app):
                        alert.last_notified = datetime.utcnow()
                        notification = NotificationLog(alert_id=alert.id, price=price)
                        db.session.add(notification)
                        logger.info(f"Notification sent for alert {alert.id}")
                    else:
                        logger.error(f"Failed to send email for alert {alert.id}")

                db.session.commit()
            except Exception as e:
                logger.exception(f"Error processing alert {alert.id}: {e}")
                db.session.rollback()