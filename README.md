# HPO Administration System

A Django-based administration system for managing Health Promotion Organizations (HPO), including questions, packages, players, and organizational data.

## Features

- **HPO Administration Portal**: Custom-branded Django admin interface
- **Question Management**: Create and manage multiple choice and true/false questions
- **Package System**: Organize questions into packages with different visibility levels
- **User Management**: Handle players, administrators, and organizations
- **API Endpoints**: JSON API for unauthenticated access to questions and packages
- **Analytics**: Track attempts, scores, and completion rates

## Project Structure

```
hpo_admin/
├── hpo/                   # Main Django project
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI application
├── hpo_app/               # Main application
│   ├── models.py          # Database models
│   ├── admin.py           # Admin interface configuration
│   ├── views.py           # API views
│   ├── urls.py            # App URL configuration
│   ├── forms.py           # Custom forms
│   └── migrations/        # Database migrations
├── templates/             # Custom templates
│   └── admin/             # Admin interface templates
├── static/                # Static files
├── manage.py              # Django management script
└── db.sqlite3            # SQLite database
```

## Models

### Core Models
- **Organisation**: Manage organizations with payment status and contact info
- **Admin**: System administrators with roles and access levels
- **Player**: End users who can take quizzes and join groups
- **Group**: Player groups with levels and creators

### Question System
- **Question**: Individual questions (multiple choice or true/false) with card associations and admin tracking
- **QuestionPackage**: Collections of questions with metadata
- **OrganizationalPackage**: Organization-specific packages
- **PublicPackage**: Publicly available packages
- **PackageAttempt**: Track user attempts and scores

## Key Features

### Card Association System
- Each question can be associated with a playing card (Spades 3-Ace, Hearts 3-Ace, Clubs 3-Ace, Diamonds 3-Ace)
- Cards have point values: 7s = 10 points, Jacks = 3, Queens = 2, Kings = 4, Aces = 11, others = 0
- API endpoint to filter questions by specific card
- Simple card selection interface without images/styles

### Admin Tracking
- Questions track which admin user created them via `created_by` field
- Admin information included in API responses
- Questions are managed through the HPO Administration interface

### API Features
- Unauthenticated access to questions and packages
- JSON responses with comprehensive question data including card information
- POST endpoint for filtering questions by card
- Consistent response format across all endpoints

## API Endpoints

The system provides JSON API endpoints for unauthenticated access:

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/{id}/` - Get specific question details
- `POST /api/questions/by-card/` - Get questions by card (payload: `{"card": "S7"}`) *[Available in local development]*

### Packages
- `GET /api/packages/` - List all published packages
- `GET /api/packages/{id}/questions/` - Get questions from a specific package

### Testing the API

#### Local Development
```bash
# Test locally (with by-card endpoint)
curl -X POST http://127.0.0.1:8000/api/questions/by-card/ \
  -H "Content-Type: application/json" \
  -d '{"card": "S3"}'
```

#### Production (Render)
```bash
# Test deployed version (basic endpoints only)
curl https://hpo-admin.onrender.com/api/questions/
curl https://hpo-admin.onrender.com/api/packages/
```

**Note**: The deployed version on Render may not include the latest features like the `by-card` endpoint. Redeploy to include recent changes.

### Example API Response
```json
{
    "success": true,
    "count": 5,
    "questions": [
        {
            "id": 1,
            "question_text": "Django is a Python web framework.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Django is indeed a high-level Python web framework...",
            "points": 1,
            "difficulty": "easy",
            "card": {
                "id": "S7",
                "suit": "Spades",
                "value": "7",
                "pointValue": 10,
                "symbol": "♠"
            },
            "created_by": "John Admin",
            "created_at": "2025-08-22T21:22:20.526631+00:00"
        }
    ]
}
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hpo_admin
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python3 manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python3 manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python3 manage.py collectstatic
   ```

7. **Start development server**
   ```bash
   python3 manage.py runserver
   ```

## Usage

### Admin Interface
1. Access the admin interface at `http://127.0.0.1:8000/admin/`
2. **Note**: Visiting the root URL `http://127.0.0.1:8000/` will automatically redirect to the admin interface
3. Login with your superuser credentials
4. The interface will display as "HPO Administration"

### API Usage
Access the API endpoints without authentication:
- Questions: `http://127.0.0.1:8000/api/questions/`
- Packages: `http://127.0.0.1:8000/api/packages/`

### Creating Questions
1. Go to the Questions section in the admin
2. Click "Add Question"
3. Fill in the question text and select type
4. For multiple choice: Add 2-4 options
5. For true/false: Options are automatically set
6. Set the correct answer and optional explanation
7. Optionally associate with a playing card
8. The creating admin will be automatically tracked

### Managing Packages
1. Create questions first
2. Go to Question Packages
3. Set package details (name, description, type)
4. Add questions to the package
5. Set visibility and status

## Deployment on Render

### Prerequisites
1. Fork or clone this repository to your GitHub account
2. Create a [Render](https://render.com) account

### Deployment Steps

#### Method 1: Using Render Dashboard
1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `hpo-admin` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn hpo.wsgi:application`
   - **Instance Type**: `Free` (or `Starter` for better performance)

3. **Environment Variables**
   Set these environment variables in Render:
   ```
   DEBUG=False
   SECRET_KEY=[auto-generated by Render]
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=your-email@example.com
   DJANGO_SUPERUSER_PASSWORD=your-secure-password
   ```

4. **Database Setup**
   - Create a PostgreSQL database on Render
   - The `DATABASE_URL` will be automatically set

#### Method 2: Using render.yaml (Infrastructure as Code)
1. Push the `render.yaml` file to your repository
2. Go to Render Dashboard → "New +" → "Blueprint"
3. Connect your repository and deploy

### Post-Deployment
1. **Access Admin Panel**: `https://your-app.onrender.com/admin/` or just `https://your-app.onrender.com/` (auto-redirects)
2. **Login**: Use the superuser credentials you set
3. **API Endpoints**: 
   - Questions: `https://your-app.onrender.com/api/questions/`
   - Packages: `https://your-app.onrender.com/api/packages/`
   - Questions by Card: `https://your-app.onrender.com/api/questions/by-card/` *(requires redeployment with latest code)*

**Important**: After making changes to your code, push to GitHub and redeploy on Render to see the latest features.

### Environment Variables for Production
- `DEBUG`: Set to `False`
- `SECRET_KEY`: Auto-generated secure key
- `DATABASE_URL`: Auto-configured PostgreSQL connection
- `DJANGO_SUPERUSER_USERNAME`: Admin username
- `DJANGO_SUPERUSER_EMAIL`: Admin email
- `DJANGO_SUPERUSER_PASSWORD`: Secure admin password

### Files Added for Deployment
- `build.sh`: Build script for Render
- `render.yaml`: Infrastructure configuration
- `Procfile`: Alternative deployment configuration
- `.env.example`: Environment variables template
- Updated `requirements.txt`: Production dependencies
- Updated `settings.py`: Production-ready configuration

## Configuration

### Admin Interface Customization
The admin interface is customized in `hpo_app/admin.py`:
```python
admin.site.site_header = "HPO Administration"
admin.site.site_title = "HPO Admin Portal"
admin.site.index_title = "Welcome to HPO Administration"
```

### Database
- Default: SQLite (`db.sqlite3`)
- Can be configured in `hpo/settings.py` for PostgreSQL, MySQL, etc.

## Development

### Adding New Models
1. Define model in `hpo_app/models.py`
2. Create migration: `python3 manage.py makemigrations`
3. Apply migration: `python3 manage.py migrate`
4. Register in admin: `hpo_app/admin.py`

### Adding API Endpoints
1. Create view in `hpo_app/views.py`
2. Add URL pattern in `hpo_app/urls.py`
3. Test endpoint functionality

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure proper `ALLOWED_HOSTS`
- API endpoints are currently open for unauthenticated access
- Consider adding rate limiting for production API usage

## License

This project is for educational and organizational use. Please ensure compliance with your organization's policies.

## Support

For questions or issues, please contact the development team or create an issue in the repository.

## Deployment Status

### Current Deployment Issue
The deployed version on `https://hpo-admin.onrender.com/` does **not** include the latest features:
- Missing `POST /api/questions/by-card/` endpoint
- Missing `created_by` field for questions
- Missing card association features

### Available on Deployment
- Basic question listing: `GET /api/questions/`
- Question details: `GET /api/questions/{id}/`
- Package listing: `GET /api/packages/`
- Package questions: `GET /api/packages/{id}/questions/`

### To Update Deployment
1. Push latest code to GitHub repository
2. Trigger redeployment on Render
3. Run migrations if needed for the `created_by` field
