# Volleyball Team Management System

A comprehensive Flask-based system for managing volleyball teams, tracking games, organizing practices, and facilitating team communication.

## Features

- **Authentication & User Management**
  - Multiple user roles (Coaches, Players, Parents)
  - Secure login/registration system
  - Profile management
  - Role-based access control

- **Team Management**
  - Team creation and roster management
  - Team achievements tracking
  - Equipment management
  - Scrapbook entries for team memories

- **Game Management**
  - Game scheduling and tracking
  - Game MVP system
  - Player game statistics
  - Real-time score updates
  - Tournament tracking

- **Practice Management**
  - Practice session scheduling
  - Attendance tracking
  - Player progress monitoring
  - Performance metrics

- **Communication System**
  - Team announcements with attachments
  - Announcement acknowledgment tracking
  - Messaging system with attachments
  - Internal communication tools

- **Broadcasting Features**
  - Live broadcast statistics
  - Broadcast chat functionality
  - Reaction system
  - Mobile broadcast support

- **Analytics & Statistics**
  - Player performance metrics
  - Team statistics
  - Season progress tracking
  - Historical data analysis
  - Comparative analytics

## Technical Features

- Database migrations support
- CSRF protection
- Secure session management
- Input validation
- File upload handling
- Email notifications
- Mobile responsiveness
- RESTful API structure

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd volleyball_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the root directory with the following variables:
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@localhost/dbname
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Default Admin Account

After initializing the database, you can log in with these credentials:
- Email: admin@example.com
- Password: adminpassword

**Important**: Change these credentials immediately after first login!

## Project Structure

```
volleyball_system/
├── app/
│   ├── auth/              # Authentication blueprint
│   ├── main/              # Main blueprint
│   ├── team/              # Team management blueprint
│   ├── game/              # Game management blueprint
│   ├── practice/          # Practice management blueprint
│   ├── communication/     # Communication blueprint
│   ├── broadcast/         # Broadcasting blueprint
│   ├── analytics/         # Analytics blueprint
│   ├── static/            # Static files
│   ├── templates/         # HTML templates
│   └── utils/             # Utility functions
├── migrations/            # Database migrations
├── logs/                  # Application logs
├── tests/                 # Test suite
├── config.py             # Configuration
├── requirements.txt      # Dependencies
└── run.py               # Application entry point
```

## Development

1. Create a new branch for your feature:
```bash
git checkout -b feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of changes"
```

3. Push your changes and create a pull request:
```bash
git push origin feature-name
```

## Testing

Run the test suite:
```bash
python -m pytest
```

## Deployment

The system is designed to be compatible with various deployment platforms, including:
- Render
- Heroku
- AWS
- DigitalOcean

For deployment instructions, see the deployment guide in the docs folder.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
