# eLearning Platform

A full-featured Django e-learning platform with role-based access control, real-time chat, course management, and RESTful API.

## Features

### Core Functionality
- **User Management**: Custom user model with Student/Teacher roles
- **Course Management**: Create, browse, enroll, and manage courses
- **Real-time Chat**: WebSocket-based global chat room using Django Channels
- **Feedback System**: Students can rate and review courses (1-5 stars)
- **Notifications**: Real-time notifications for enrollments, new materials, and feedback
- **RESTful API**: Complete API endpoints for users, courses, enrollments, and feedback
- **User Search**: Search for users by username or real name
- **Profile Management**: Upload profile pictures, update status, view user profiles

### Role-Based Features
**Teachers can:**
- Create and manage courses
- Upload course materials
- View enrolled students
- Block students from courses
- Receive notifications when students enroll or leave feedback

**Students can:**
- Browse available courses
- Enroll in courses
- Access course materials
- Leave feedback and ratings
- Receive notifications when new materials are added

## Technology Stack

- **Backend**: Django 5.1.5
- **Real-time**: Django Channels 4.2.0 + Redis
- **API**: Django REST Framework 3.15.2
- **Frontend**: Bootstrap 5 + Crispy Forms
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Server**: Daphne (ASGI) for WebSocket support
- **Testing**: pytest, pytest-django, coverage

## Installation

### Prerequisites
- Python 3.9 or higher
- Redis server (for chat functionality)

### Quick Setup

1. **Clone the repository**
```bash
cd /Users/pega/Documents/GitHub/eLearning/elearning
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. **Run the setup script**
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Install all Python dependencies
- Create necessary directories
- Run database migrations
- Collect static files
- Check Redis installation

### Manual Setup

If you prefer manual setup:

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Create media directories**
```bash
mkdir -p media/profile_pics media/course_materials
```

3. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

5. **Install and start Redis** (required for chat)
```bash
# macOS
brew install redis
redis-server --daemonize yes

# Ubuntu/Debian
sudo apt-get install redis-server
sudo service redis-server start
```

## Running the Application

### Development Server

For basic development without WebSocket support:
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

### Production Mode with WebSocket Support

Using Daphne (recommended for full functionality including chat):
```bash
daphne -p 8000 elearning.asgi:application
```

Visit: http://127.0.0.1:8000

## Creating Users

### Create Admin/Superuser
```bash
python manage.py createsuperuser
```

### Create Test Users (for development)
```bash
python create_test_users.py
```

This creates sample teachers and students:
- **Teachers**: teacher1, teacher2 (password: password123)
- **Students**: student1, student2, student3 (password: password123)

## Testing

### Run All Tests
```bash
python manage.py test
```

### Run with Coverage
```bash
# Generate coverage report
coverage run --source='.' --omit='*/asgi.py,*/wsgi.py,*/manage.py' manage.py test

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

### Run Specific App Tests
```bash
python manage.py test users
python manage.py test courses
python manage.py test chat
```

## API Endpoints

The API is available at `/api/` with the following endpoints:

- `GET /api/users/` - List all users
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create a course (teachers only)
- `GET /api/enrollments/` - List enrollments
- `POST /api/enrollments/` - Enroll in a course
- `GET /api/feedback/` - List feedback
- `POST /api/feedback/` - Submit feedback

All API endpoints require authentication.

## Project Structure

```
elearning/
├── chat/                    # Real-time chat application
│   ├── consumers.py        # WebSocket consumer
│   ├── routing.py          # WebSocket URL routing
│   └── templates/          # Chat templates
├── courses/                # Course management app
│   ├── models.py          # Course, Enrollment, Feedback, etc.
│   ├── views.py           # Course views
│   ├── api_views.py       # API endpoints
│   └── signals.py         # Notification signals
├── users/                  # User management app
│   ├── models.py          # CustomUser model
│   ├── views.py           # User views
│   ├── decorators.py      # Role-based decorators
│   └── context_processors.py  # Notification context
├── elearning/             # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL configuration
│   ├── asgi.py           # ASGI configuration
│   └── api_urls.py       # API URL router
├── templates/             # Global templates
├── static/               # Static files
└── manage.py            # Django management script
```

## Key Features Explained

### Notifications
The platform uses Django signals to create notifications:
- When a student enrolls in a course, the teacher is notified
- When new material is uploaded, all enrolled students are notified
- When feedback is submitted, the teacher is notified

Unread notification count appears in the navbar.

### Course Blocking
Teachers can block students from enrolling in their courses. Blocked students:
- Cannot enroll in the course
- Are automatically unenrolled if previously enrolled

### WebSocket Chat
The global chat room uses WebSocket connections for real-time messaging:
- Messages are broadcast to all connected users
- Shows username with each message
- Requires Redis for channel layer support

## Configuration

### Environment Variables (Production)
For production, set these environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com'
export DATABASE_URL='postgres://user:pass@localhost/dbname'
export REDIS_URL='redis://localhost:6379'
```

### Static Files (Production)
The project uses WhiteNoise for static file serving. Run:
```bash
python manage.py collectstatic
```

## Troubleshooting

### Redis Connection Error
If chat doesn't work, ensure Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### WebSocket Connection Failed
Make sure you're using Daphne instead of the default Django server:
```bash
daphne elearning.asgi:application
```

### Static Files Not Loading
Run collectstatic and check STATIC_ROOT setting:
```bash
python manage.py collectstatic --noinput
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational purposes.

