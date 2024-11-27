import pytest
from flask import current_app
from app.utils.email import send_email, send_password_reset_email
from app.auth.models import User, Role
from unittest.mock import patch

def test_send_email(app):
    """Test the send_email function."""
    with app.app_context():
        with patch('flask_mail.Mail.send') as mock_send:
            send_email(
                subject='Test Subject',
                sender='test@example.com',
                recipients=['recipient@example.com'],
                text_body='Test body',
                html_body='<p>Test body</p>'
            )
            
            # Verify that send was called
            assert mock_send.called
            
            # Get the message that would have been sent
            msg = mock_send.call_args[0][0]
            
            # Verify message properties
            assert msg.subject == 'Test Subject'
            assert msg.sender == 'test@example.com'
            assert msg.recipients == ['recipient@example.com']
            assert 'Test body' in msg.body
            assert '<p>Test body</p>' in msg.html

def test_send_password_reset_email(app):
    """Test the password reset email function."""
    with app.app_context():
        # Create a test user
        role = Role.query.filter_by(name='player').first()
        user = User(
            username='testreset',
            email='testreset@example.com',
            first_name='Test',
            last_name='Reset',
            role=role
        )
        user.password = 'password123'
        
        with patch('flask_mail.Mail.send') as mock_send:
            # Generate a test token
            token = 'test-token'
            
            # Send reset email
            send_password_reset_email(user, token)
            
            # Verify that send was called
            assert mock_send.called
            
            # Get the message that would have been sent
            msg = mock_send.call_args[0][0]
            
            # Verify message properties
            assert '[Volleyball System] Reset Your Password' in msg.subject
            assert msg.recipients == ['testreset@example.com']
            assert 'Reset Your Password' in msg.html
            assert token in msg.html
            assert token in msg.body

def test_email_config(app):
    """Test email configuration."""
    assert app.config['MAIL_SERVER'] == 'localhost.localdomain'
    assert app.config['MAIL_PORT'] == 587
    assert app.config['MAIL_USE_TLS'] is True

@pytest.mark.parametrize('template_name', [
    'reset_password.html',
    'reset_password.txt'
])
def test_email_templates_exist(app, template_name):
    """Test that email templates exist and can be rendered."""
    with app.app_context():
        from flask import render_template
        
        # Create test user and token
        user = User(
            username='templatetest',
            email='template@test.com',
            first_name='Template',
            last_name='Test',
            role=Role.query.filter_by(name='player').first()
        )
        token = 'test-token'
        
        # Attempt to render template
        rendered = render_template(f'email/{template_name}',
                                user=user,
                                token=token)
        
        # Verify basic content
        assert rendered is not None
        assert len(rendered) > 0
        assert token in rendered

def test_async_email_sending(app):
    """Test asynchronous email sending."""
    with app.app_context():
        with patch('threading.Thread.start') as mock_start:
            send_email(
                subject='Async Test',
                sender='test@example.com',
                recipients=['async@example.com'],
                text_body='Async test',
                html_body='<p>Async test</p>'
            )
            
            # Verify that a thread was started
            assert mock_start.called

def test_email_error_handling(app):
    """Test email error handling."""
    with app.app_context():
        with patch('flask_mail.Mail.send', side_effect=Exception('Test error')):
            # The email function should not raise an exception
            # even if sending fails
            send_email(
                subject='Error Test',
                sender='test@example.com',
                recipients=['error@example.com'],
                text_body='Error test',
                html_body='<p>Error test</p>'
            )

def test_email_content_security(app):
    """Test email content security measures."""
    with app.app_context():
        with patch('flask_mail.Mail.send') as mock_send:
            # Test with potentially malicious content
            malicious_content = '<script>alert("xss")</script>'
            
            send_email(
                subject='Security Test',
                sender='test@example.com',
                recipients=['security@example.com'],
                text_body='Security test',
                html_body=f'<p>{malicious_content}</p>'
            )
            
            msg = mock_send.call_args[0][0]
            
            # Verify that script tags are escaped or removed
            assert '<script>' not in msg.html
            assert 'alert' not in msg.html

def test_email_rate_limiting(app):
    """Test email rate limiting if implemented."""
    with app.app_context():
        with patch('flask_mail.Mail.send') as mock_send:
            # Send multiple emails in quick succession
            for i in range(10):
                send_email(
                    subject=f'Rate Test {i}',
                    sender='test@example.com',
                    recipients=['rate@example.com'],
                    text_body=f'Rate test {i}',
                    html_body=f'<p>Rate test {i}</p>'
                )
            
            # Verify that all emails were queued
            assert mock_send.call_count == 10

def test_email_template_inheritance(app):
    """Test email template inheritance and styling."""
    with app.app_context():
        from flask import render_template
        
        # Test user
        user = User(
            username='styletest',
            email='style@test.com',
            first_name='Style',
            last_name='Test',
            role=Role.query.filter_by(name='player').first()
        )
        token = 'test-token'
        
        # Render HTML template
        rendered = render_template('email/reset_password.html',
                                user=user,
                                token=token)
        
        # Check for styling elements
        assert 'style' in rendered.lower()
        assert 'font-family' in rendered.lower()
        assert 'color' in rendered.lower()
