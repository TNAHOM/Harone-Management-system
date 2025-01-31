# SWIFT Connect Onboarding System

A comprehensive customer relationship management system designed for SWIFT network connectivity onboarding. This system streamlines business customer documentation processing and management.

[IMAGE-HERE]

## Core Features

### Authentication System 🔐
- Secure login and registration system
- Role-based access control (Business, Processor, Auditor, Admin)
- Session management and security
- Business customer self-registration

[IMAGE-HERE]

### Business Customer Portal 💼
- Self-service onboarding request submission
- Document upload system (Business License, Tax ID)
- Real-time request status tracking
- Multiple business types support (Sole Proprietorship, Partnership, Corporation, LLC)

[IMAGE-HERE]

### CRM Dashboard 📊
- Request queue management system
- Status filtering (All, Pending, Approved, Rejected)
- Document review interface
- Request processing workflow
- Detailed request information display
- Comments and feedback system

[IMAGE-HERE]

### Admin Management ⚙️
- User management interface
- Internal user creation (Processor, Auditor, Admin roles)
- System statistics dashboard
- User verification status tracking
- Business customer overview

### Document Management 📁
- Secure document upload system
- Support for multiple file formats (PDF, JPG, JPEG, PNG)
- Document download functionality
- Business license and tax ID management

## Technology Stack

- **Backend**: Python Flask
- **Database**: MariaDB 10.6
- **Frontend**: Bootstrap 5
- **Template Engine**: Jinja2
- **JavaScript**: jQuery 3.7.1
- **Container**: Docker

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- MariaDB 10.6+ (handled by Docker)
- Modern web browser

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd swift-connect
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   ```
   http://localhost:5000
   ```

[IMAGE-HERE]

## Local Development Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure database:
   ```bash
   flask db upgrade
   ```

4. Run the application:
   ```bash
   flask run
   ```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/register` - Business customer registration

### Requests
- `GET /requests` - List requests
- `POST /requests` - Create new request
- `GET /requests/<id>` - Get request details
- `PUT /requests/<id>` - Update request status
- `GET /requests/<id>/documents` - Download documents

### Admin
- `GET /admin/users` - List all users
- `POST /admin/users` - Create internal user
- `GET /admin/process_request/<id>` - Process onboarding request

## Environment Variables

```
FLASK_APP=run.py
FLASK_ENV=development/production
DATABASE_URL=mysql://user:pass@localhost/db
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.server.com
MAIL_PORT=587
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
UPLOAD_FOLDER=path/to/uploads
```

## Docker Configuration

The application uses Docker Compose with:
- MariaDB 10.6 database service
- Persistent volume for database storage
- Exposed ports:
  - Database: 3306
  - Web application: 5000

## User Roles

1. **Business Customer**
   - Account registration
   - Onboarding request submission
   - Document upload
   - Request status tracking

2. **CRM Processor**
   - Review onboarding requests
   - Approve/reject submissions
   - Add processing comments
   - Access document downloads

3. **Administrator**
   - Manage system users
   - Create internal accounts
   - View system statistics
   - Monitor user verification

4. **Auditor**
   - View all requests
   - Monitor request processing
   - Access system reports
   - Track request statuses

## Security Features

- Password-based authentication
- Role-based access control
- Secure file upload handling
- CSRF protection
- Session management
- Input validation