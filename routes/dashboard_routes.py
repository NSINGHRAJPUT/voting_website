from flask import Blueprint, render_template, session, redirect, url_for
from models import User, Vote, db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    votes = Vote.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, votes=votes)
