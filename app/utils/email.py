from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Send email asynchronously
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user, token):
    send_email(
        '[Volleyball System] Reset Your Password',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                user=user, token=token)
    )

def send_team_invitation_email(user, team, token):
    send_email(
        f'[Volleyball System] Invitation to join {team.name}',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/team_invitation.txt',
                                user=user, team=team, token=token),
        html_body=render_template('email/team_invitation.html',
                                user=user, team=team, token=token)
    )

def send_announcement_email(announcement, recipients):
    send_email(
        f'[Volleyball System] New Announcement: {announcement.title}',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email for user in recipients],
        text_body=render_template('email/announcement.txt',
                                announcement=announcement),
        html_body=render_template('email/announcement.html',
                                announcement=announcement)
    )

def send_practice_reminder_email(practice, recipients):
    send_email(
        f'[Volleyball System] Practice Reminder: {practice.title}',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email for user in recipients],
        text_body=render_template('email/practice_reminder.txt',
                                practice=practice),
        html_body=render_template('email/practice_reminder.html',
                                practice=practice)
    )

def send_game_reminder_email(game, recipients):
    send_email(
        f'[Volleyball System] Game Reminder: {game.title}',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email for user in recipients],
        text_body=render_template('email/game_reminder.txt',
                                game=game),
        html_body=render_template('email/game_reminder.html',
                                game=game)
    )
