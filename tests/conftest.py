import os
import tempfile
import pytest
from app import create_app, db
from app.auth.models import User, Role

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain'
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        
        # Create roles
        admin_role = Role(name='admin')
        coach_role = Role(name='coach')
        player_role = Role(name='player')
        parent_role = Role(name='parent')
        
        db.session.add_all([admin_role, coach_role, player_role, parent_role])
        db.session.commit()
        
        # Create test admin user
        admin = User(
            username='testadmin',
            email='admin@test.com',
            first_name='Test',
            last_name='Admin',
            role=admin_role
        )
        admin.password = 'password123'
        
        # Create test coach user
        coach = User(
            username='testcoach',
            email='coach@test.com',
            first_name='Test',
            last_name='Coach',
            role=coach_role
        )
        coach.password = 'password123'
        
        # Create test player user
        player = User(
            username='testplayer',
            email='player@test.com',
            first_name='Test',
            last_name='Player',
            role=player_role
        )
        player.password = 'password123'
        
        db.session.add_all([admin, coach, player])
        db.session.commit()

    yield app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    """Authentication helper class for tests."""
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def login(self, email='admin@test.com', password='password123'):
            return self._client.post(
                '/auth/login',
                data={'email': email, 'password': password}
            )

        def logout(self):
            return self._client.get('/auth/logout')

        def register(self, username='testuser', email='user@test.com',
                    password='password123', confirm_password='password123',
                    first_name='Test', last_name='User', role='player',
                    phone='1234567890'):
            return self._client.post(
                '/auth/register',
                data={
                    'username': username,
                    'email': email,
                    'password': password,
                    'confirm_password': confirm_password,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'phone': phone
                }
            )

    return AuthActions(client)

@pytest.fixture
def logged_in_admin(auth, client):
    """A logged-in admin user."""
    auth.login()
    return client

@pytest.fixture
def logged_in_coach(auth, client):
    """A logged-in coach user."""
    auth.login(email='coach@test.com', password='password123')
    return client

@pytest.fixture
def logged_in_player(auth, client):
    """A logged-in player user."""
    auth.login(email='player@test.com', password='password123')
    return client
