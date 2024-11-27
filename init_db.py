import os
from app import create_app, db
from app.auth.models import Role, User
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize the database with required roles and admin user."""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Creating roles...")
        # Create roles if they don't exist
        roles = ['admin', 'coach', 'player', 'parent']
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name)
                db.session.add(role)
                print(f"Created role: {role_name}")
        
        try:
            db.session.commit()
            print("Roles created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating roles: {str(e)}")
            return
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(email='admin@example.com').first():
            print("\nCreating admin user...")
            admin_role = Role.query.filter_by(name='admin').first()
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('adminpassword'),
                first_name='Admin',
                last_name='User',
                role=admin_role,
                is_active=True
            )
            db.session.add(admin_user)
            
            try:
                db.session.commit()
                print("Admin user created successfully!")
                print("\nAdmin credentials:")
                print("Email: admin@example.com")
                print("Password: adminpassword")
                print("\nPlease change these credentials after first login!")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating admin user: {str(e)}")
                return
        
        print("\nDatabase initialization completed successfully!")

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    app = create_app('development')
    uploads_dir = os.path.join(app.root_path, 'static', 'profile_pics')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"Created uploads directory: {uploads_dir}")
    
    # Create the logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(app.root_path), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    
    # Initialize the database
    init_db()
