# Little Flower International School - Web Application

## Overview

This is a Flask-based web application for Little Flower International School, featuring both a public website and an admin panel for content management. The application provides comprehensive school information, news management, faculty profiles, admission processing, and contact handling.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLite (development) with SQLAlchemy ORM, MySQL support via PyMySQL
- **Authentication**: Flask-Login for admin authentication
- **File Handling**: Local file storage with Werkzeug utilities
- **Forms**: WTForms for form validation and rendering

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **CSS Framework**: Bootstrap 5.3.0
- **JavaScript Libraries**: 
  - AOS (Animate On Scroll) for animations
  - Font Awesome for icons
  - Custom JavaScript for interactive features
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Application Structure
```
/
├── app.py (Flask application configuration)
├── main.py (Application entry point)
├── models.py (Database models)
├── forms.py (WTForms classes)
├── routes.py (Public website routes)
├── admin.py (Admin panel routes)
├── utils.py (Utility functions)
├── templates/ (HTML templates)
├── static/ (CSS, JS, images)
└── uploads/ (File uploads directory)
```

## Key Components

### Database Models
- **User**: Admin user authentication
- **SchoolInfo**: Dynamic school content (about, mission, vision, etc.)
- **News**: News articles and announcements
- **Faculty**: Faculty member profiles
- **Contact**: Contact form submissions
- **Admission**: Admission application tracking
- **Gallery**: Image gallery management
- **Document**: File/document management
- **Event**: School events and activities

### Public Website Features
- Homepage with featured content
- About Us section with mission/vision
- Academic information
- Faculty profiles
- News and updates
- Gallery
- Contact forms
- Admission applications
- Resource downloads

### Admin Panel Features
- Dashboard with statistics
- Content management system
- News article management
- Faculty profile management
- Contact message handling
- Admission application processing
- Gallery management
- Document/resource management
- User authentication and authorization

## Data Flow

1. **Public Users**: Access website → View content → Submit forms (contact/admission)
2. **Admin Users**: Login → Access admin panel → Manage content → Database updates
3. **Content Flow**: Database → SQLAlchemy ORM → Flask routes → Jinja2 templates → HTML output
4. **File Uploads**: Form submission → Werkzeug file handling → Local storage → Database reference

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-WTF (form handling)
- WTForms (form validation)
- Werkzeug (utilities)
- Pillow (image processing)

### Frontend Libraries
- Bootstrap 5.3.0 (CSS framework)
- Font Awesome 6.4.0 (icons)
- AOS 2.3.1 (scroll animations)
- Google Fonts (Poppins, Inter)

### Development Tools
- SQLite (database)
- Python logging
- Environment variables for configuration

## Deployment Strategy

### Environment Configuration
- `SESSION_SECRET`: Flask session secret key
- `DATABASE_URL`: Database connection string (defaults to SQLite)
  - For MySQL: `mysql+pymysql://username:password@host/database`
  - For SQLite: `sqlite:///database.db`
- File upload directory: `uploads/` (auto-created)

### Production Considerations
- Database can be upgraded to PostgreSQL by changing `DATABASE_URL`
- Static files should be served by web server (nginx/Apache)
- File uploads should be moved to cloud storage for scalability
- Environment variables for security configuration
- WSGI server (Gunicorn) for production deployment

### Security Features
- CSRF protection via Flask-WTF
- File upload restrictions and validation
- Admin authentication required for sensitive operations
- Input validation and sanitization
- Secure session management

## Changelog
- July 03, 2025. Initial setup
- July 03, 2025. Added MySQL support via PyMySQL driver, configurable via DATABASE_URL environment variable

## User Preferences

Preferred communication style: Simple, everyday language.