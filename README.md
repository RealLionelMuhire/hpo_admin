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
├── hpo/                    # Main Django project
│   ├── settings.py         # Django settings
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
- **Question**: Individual questions (multiple choice or true/false)
- **QuestionPackage**: Collections of questions with metadata
- **OrganizationalPackage**: Organization-specific packages
- **PublicPackage**: Publicly available packages
- **PackageAttempt**: Track user attempts and scores

## API Endpoints

The system provides JSON API endpoints for unauthenticated access:

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/{id}/` - Get specific question details

### Packages
- `GET /api/packages/` - List all published packages
- `GET /api/packages/{id}/questions/` - Get questions from a specific package

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
            "created_at": "2025-08-20T21:22:20.526631+00:00"
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
2. Login with your superuser credentials
3. The interface will display as "HPO Administration"

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

### Managing Packages
1. Create questions first
2. Go to Question Packages
3. Set package details (name, description, type)
4. Add questions to the package
5. Set visibility and status

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
