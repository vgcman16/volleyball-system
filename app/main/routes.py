from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import main
from app.auth.models import User, Role
from app import db

@main.route('/')
def index():
    """Home page route."""
    stats = {
        'total_users': User.query.count(),
        'total_teams': db.session.query(db.func.count(db.distinct(User.teams))).scalar(),
        'total_coaches': User.query.join(Role).filter(Role.name == 'coach').count(),
        'total_players': User.query.join(Role).filter(Role.name == 'player').count()
    }
    
    if current_user.is_authenticated:
        user_teams = current_user.teams
        upcoming_games = []  # Will be implemented with Game model
        upcoming_practices = []  # Will be implemented with Practice model
        recent_announcements = []  # Will be implemented with Announcement model
        
        return render_template('main/dashboard.html',
                             stats=stats,
                             user_teams=user_teams,
                             upcoming_games=upcoming_games,
                             upcoming_practices=upcoming_practices,
                             recent_announcements=recent_announcements)
    
    return render_template('main/index.html', stats=stats)

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page route."""
    return redirect(url_for('main.index'))

@main.route('/about')
def about():
    """About page route."""
    return render_template('main/about.html')

@main.route('/contact')
def contact():
    """Contact page route."""
    return render_template('main/contact.html')

@main.route('/privacy')
def privacy():
    """Privacy policy page route."""
    return render_template('main/privacy.html')

@main.route('/terms')
def terms():
    """Terms of service page route."""
    return render_template('main/terms.html')

@main.app_errorhandler(404)
def not_found_error(error):
    """404 error handler."""
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    """500 error handler."""
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main.app_errorhandler(403)
def forbidden_error(error):
    """403 error handler."""
    return render_template('errors/403.html'), 403
