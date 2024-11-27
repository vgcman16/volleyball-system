import os
from app import create_app, db
from app.auth.models import User, Role
from flask_migrate import upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate database to latest revision
    upgrade()

    # Create or update roles
    Role.query.delete()
    roles = ['admin', 'coach', 'player', 'parent']
    for role_name in roles:
        role = Role(name=role_name)
        db.session.add(role)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

    # Create admin user if it doesn't exist
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role and not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            role=admin_role
        )
        admin.password = 'adminpassword'  # Change this in production!
        db.session.add(admin)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

@app.shell_context_processor
def make_shell_context():
    """Configure Flask shell context."""
    return {
        'db': db,
        'User': User,
        'Role': Role
    }

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    uploads_dir = os.path.join(app.root_path, 'static', 'profile_pics')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Create the logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    app.run(debug=True)
