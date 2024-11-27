import pytest
from flask import session, g
from app.auth.models import User, Role
from app import db

def test_index_page(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    # Check for key elements in the landing page
    assert b'Volleyball Team Management System' in response.data
    assert b'Get Started' in response.data
    assert b'Sign In' in response.data
    
    # Check for feature sections
    assert b'Game Management' in response.data
    assert b'Practice Planning' in response.data
    assert b'Team Communication' in response.data
    assert b'Performance Analytics' in response.data

def test_dashboard_access(client, auth):
    """Test dashboard access and content."""
    # Redirect to login when not authenticated
    response = client.get('/dashboard')
    assert response.headers['Location'].startswith('/auth/login')
    
    # Access dashboard when authenticated
    auth.login()
    response = client.get('/dashboard')
    assert response.headers['Location'] == '/'  # Redirects to index which shows dashboard for authenticated users
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome back' in response.data
    assert b'My Teams' in response.data
    assert b'Upcoming Games' in response.data
    assert b'Upcoming Practices' in response.data
    assert b'Recent Announcements' in response.data

def test_about_page(client):
    """Test the about page."""
    response = client.get('/about')
    assert response.status_code == 200
    # Add assertions for about page content when implemented

def test_contact_page(client):
    """Test the contact page."""
    response = client.get('/contact')
    assert response.status_code == 200
    # Add assertions for contact page content when implemented

def test_privacy_page(client):
    """Test the privacy policy page."""
    response = client.get('/privacy')
    assert response.status_code == 200
    # Add assertions for privacy page content when implemented

def test_terms_page(client):
    """Test the terms of service page."""
    response = client.get('/terms')
    assert response.status_code == 200
    # Add assertions for terms page content when implemented

def test_404_error(client):
    """Test 404 error page."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'Page not found' in response.data
    assert b'The page you\'re looking for doesn\'t exist' in response.data

def test_500_error(app, client):
    """Test 500 error page."""
    # Create a test route that raises an error
    @app.route('/error-test')
    def error_test():
        raise Exception('Test error')
    
    response = client.get('/error-test')
    assert response.status_code == 500
    assert b'Internal Server Error' in response.data
    assert b'Something went wrong on our end' in response.data

def test_403_error(client, auth):
    """Test 403 error page."""
    # Create a test route that requires admin access
    @client.application.route('/admin-only')
    def admin_only():
        user = User.query.filter_by(email='player@test.com').first()
        if user.role.name != 'admin':
            return 'Forbidden', 403
        return 'Admin Page'
    
    # Test as player (should get 403)
    auth.login('player@test.com', 'password123')
    response = client.get('/admin-only')
    assert response.status_code == 403
    assert b'Access Forbidden' in response.data
    assert b'you don\'t have permission to access this page' in response.data

def test_stats_display(client, app):
    """Test that statistics are correctly displayed on the index page."""
    with app.app_context():
        response = client.get('/')
        assert response.status_code == 200
        
        # Get actual counts from database
        total_users = User.query.count()
        total_coaches = User.query.join(Role).filter(Role.name == 'coach').count()
        total_players = User.query.join(Role).filter(Role.name == 'player').count()
        
        # Convert counts to strings and check if they appear in the response
        assert str(total_users).encode() in response.data
        assert str(total_coaches).encode() in response.data
        assert str(total_players).encode() in response.data

def test_dashboard_components(client, auth, app):
    """Test that dashboard components are properly displayed for different roles."""
    auth.login()
    response = client.get('/')
    
    # Common components for all roles
    assert b'My Teams' in response.data
    assert b'Upcoming Games' in response.data
    assert b'Upcoming Practices' in response.data
    assert b'Recent Announcements' in response.data
    
    # Admin/Coach specific components
    if User.query.filter_by(email='admin@test.com').first().role.name in ['admin', 'coach']:
        assert b'Create Team' in response.data
        assert b'Analytics' in response.data

def test_navigation_menu(client, auth):
    """Test that navigation menu shows correct links based on authentication status."""
    # Test navigation for unauthenticated user
    response = client.get('/')
    assert b'Login' in response.data
    assert b'Register' in response.data
    assert b'Teams' not in response.data
    
    # Test navigation for authenticated user
    auth.login()
    response = client.get('/')
    assert b'Teams' in response.data
    assert b'Games' in response.data
    assert b'Practices' in response.data
    assert b'Announcements' in response.data
    assert b'Profile' in response.data
    assert b'Logout' in response.data
