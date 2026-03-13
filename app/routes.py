from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Alert

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    total_alerts = Alert.query.count()
    active_alerts = Alert.query.filter_by(active=True).count()
    return render_template('index.html', total=total_alerts, active=active_alerts)

@bp.route('/alerts')
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return render_template('alerts.html', alerts=alerts)

@bp.route('/alerts/create', methods=['GET', 'POST'])
def create_alert():
    if request.method == 'POST':
        asset_symbol = request.form['asset_symbol'].strip().upper()
        asset_type = request.form['asset_type']
        condition = request.form['condition']
        threshold = float(request.form['threshold'])
        email = request.form['email'].strip()

        if not all([asset_symbol, asset_type, condition, threshold, email]):
            flash('All fields are required.')
            return redirect(url_for('main.create_alert'))

        alert = Alert(
            asset_symbol=asset_symbol,
            asset_type=asset_type,
            condition=condition,
            threshold=threshold,
            email=email,
            active=True
        )
        db.session.add(alert)
        db.session.commit()
        flash('Alert created successfully!')
        return redirect(url_for('main.list_alerts'))

    return render_template('create_alert.html')

@bp.route('/alerts/<int:alert_id>/delete', methods=['POST'])
def delete_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.active = False
    db.session.commit()
    flash('Alert deactivated.')
    return redirect(url_for('main.list_alerts'))

@bp.route('/alerts/<int:alert_id>/activate', methods=['POST'])
def activate_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.active = True
    db.session.commit()
    flash('Alert activated.')
    return redirect(url_for('main.list_alerts'))