from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Configure login settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.team import team as team_blueprint
    app.register_blueprint(team_blueprint, url_prefix='/team')
    
    from app.game import game as game_blueprint
    app.register_blueprint(game_blueprint, url_prefix='/game')
    
    from app.practice import practice as practice_blueprint
    app.register_blueprint(practice_blueprint, url_prefix='/practice')
    
    from app.communication import communication as communication_blueprint
    app.register_blueprint(communication_blueprint, url_prefix='/communication')
    
    from app.broadcast import broadcast as broadcast_blueprint
    app.register_blueprint(broadcast_blueprint, url_prefix='/broadcast')
    
    from app.analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')

    return app
