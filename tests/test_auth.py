import pytest
from flask import session, g
from app.auth.models import User, Role
from app import db

def test_register(client, app):
    """Test registration functionality."""
    # Test GET request
    assert client.get('/auth/register').status_code == 200
    
    # Test successful registration
    response = client.post(
        '/auth/register',
        data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'player',
            'phone': '1234567890'
        }
    )
    assert response.headers['Location'] == '/auth/login'
    
    # Verify user was created
    with app.app_context():
        assert User.query.filter_by(email='newuser@test.com').first() is not None

def test_register_validation(client):
    """Test registration validation."""
    # Test duplicate email
    response = client.post(
        '/auth/register',
        data={
            'username': 'testuser',
            'email': 'admin@test.com',  # Already exists
            'password': 'password123',
            'confirm_password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'player',
            'phone': '1234567890'
        }
    )
    assert b'Email already registered' in response.data
    
    # Test password mismatch
    response = client.post(
        '/auth/register',
        data={
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'password123',
            'confirm_password': 'password456',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'player',
            'phone': '1234567890'
        }
    )
    assert b'Passwords must match' in response.data

def test_login(client, auth):
    """Test login functionality."""
    # Test GET request
    assert client.get('/auth/login').status_code == 200
    
    # Test successful login
    response = auth.login()
    assert response.headers['Location'] == '/'
    
    # Test user is logged in
    with client:
        client.get('/')
        assert session['_user_id'] is not None

def test_login_validation(auth):
    """Test login validation."""
    # Test invalid email
    response = auth.login('wrong@test.com', 'password123')
    assert b'Invalid email or password' in response.data
    
    # Test invalid password
    response = auth.login('admin@test.com', 'wrongpassword')
    assert b'Invalid email or password' in response.data

def test_logout(client, auth):
    """Test logout functionality."""
    auth.login()
    
    with client:
        auth.logout()
        assert '_user_id' not in session

def test_password_reset_request(client, app):
    """Test password reset request functionality."""
    # Test GET request
    assert client.get('/auth/reset_password_request').status_code == 200
    
    # Test with valid email
    response = client.post(
        '/auth/reset_password_request',
        data={'email': 'admin@test.com'}
    )
    assert b'Check your email for instructions to reset your password' in response.data
    
    # Test with invalid email
    response = client.post(
        '/auth/reset_password_request',
        data={'email': 'nonexistent@test.com'}
    )
    assert b'No account found with that email address' in response.data

def test_profile(client, auth):
    """Test profile functionality."""
    # Login required
    assert client.get('/auth/profile').headers['Location'].startswith('/auth/login')
    
    auth.login()
    
    # Test GET request
    response = client.get('/auth/profile')
    assert response.status_code == 200
    assert b'Profile Settings' in response.data
    
    # Test profile update
    response = client.post(
        '/auth/profile',
        data={
            'username': 'updatedadmin',
            'email': 'admin@test.com',
            'first_name': 'Updated',
            'last_name': 'Admin',
            'phone': '9876543210'
        }
    )
    assert response.headers['Location'] == '/auth/profile'
    
    # Verify changes
    response = client.get('/auth/profile')
    assert b'Updated' in response.data
    assert b'9876543210' in response.data

def test_role_based_access(client, auth, app):
    """Test role-based access control."""
    # Create a test route that requires admin role
    @app.route('/admin_only')
    def admin_only():
        user = User.query.filter_by(email='admin@test.com').first()
        if user.role.name != 'admin':
            return 'Forbidden', 403
        return 'Admin Page'
    
    # Test access as admin
    auth.login()
    assert client.get('/admin_only').status_code == 200
    
    # Test access as player
    auth.login('player@test.com', 'password123')
    assert client.get('/admin_only').status_code == 403

def test_user_model(app):
    """Test User model functionality."""
    with app.app_context():
        # Test password hashing
        user = User(
            username='testuser',
            email='test@test.com',
            first_name='Test',
            last_name='User',
            role=Role.query.filter_by(name='player').first()
        )
        user.password = 'password123'
        
        assert user.password_hash is not None
        assert user.password_hash != 'password123'
        assert user.verify_password('password123')
        assert not user.verify_password('wrongpassword')
        
        # Test full name property
        assert user.get_full_name() == 'Test User'

def test_unauthorized_access(client):
    """Test unauthorized access to protected routes."""
    protected_routes = [
        '/auth/profile',
        '/team/create',
        '/game/create',
        '/practice/create'
    ]
    
    for route in protected_routes:
        response = client.get(route)
        assert response.headers['Location'].startswith('/auth/login')
