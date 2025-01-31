# SWIFT Connect Onboarding System

A comprehensive customer relationship management system designed for SWIFT network connectivity onboarding. This system streamlines business customer documentation processing and management.

![Docker Container](screenshoots/docker-container.png)

## Core Features

### Authentication System 🔐
- Secure login and registration system
- Role-based access control (Business, Processor, Auditor, Admin)
- Session management and security
- Business customer self-registration

![Business Customer Signup Page](screenshoots/buissness-customer-signup-page.png)

### Business Customer Portal 💼
- Self-service onboarding request submission
- Document upload system (Business License, Tax ID)
- Real-time request status tracking
- Multiple business types support (Sole Proprietorship, Partnership, Corporation, LLC)

![Business Customer Dashboard Page](screenshoots/buissness-customer-dashboard-page.png)
![Business Customer Onboarding Request Popup Page](screenshoots/buissness-customer-onboarding-request-popup-page.png)

### CRM Dashboard 📊
- Request queue management system
- Status filtering (All, Pending, Approved, Rejected)
- Document review interface
- Request processing workflow
- Detailed request information display
- Comments and feedback system

![Business Customer Request Detail Page](screenshoots/buissness-customer-request-detail-page.png)
![Admin Review Request Popup](screenshoots/admin-review-request-popup.png)

### Admin Management ⚙️
- User management interface
- Internal user creation (Processor, Auditor, Admin roles)
- System statistics dashboard
- User verification status tracking
- Business customer overview

![Admin Dashboard Page](screenshoots/admin-dashboard-page.png)
![Admin User Management Page](screenshoots/admin-usermanagment-page.png)

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

3. Start the MariaDB service:
   ```bash
   docker-compose up -d db
   ```

4. Access the application:
   ```
   http://localhost:5000
   ```

Note: The application itself is not containerized. Only the MariaDB database is run in a Docker container. Follow the Local Development Setup for running the application.

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

![Auditor Dashboard Page](screenshoots/auditor-dashboard-page.png)

## Security Features

- Password-based authentication
- Role-based access control
- Secure file upload handling
- CSRF protection
- Session management
- Input validation

## Support

For technical support and inquiries:
- Email: support@swiftconnect.com
- Issue Tracking: GitHub Issues

## User Profiles and Requirements

### User Profiles

1. **Business Customer**
   - Needs to submit onboarding requests and track their status.
   - Requires a user-friendly interface for document uploads and status updates.

2. **CRM Processor**
   - Responsible for reviewing and processing onboarding requests.
   - Needs efficient tools for filtering, reviewing, and updating request statuses.

3. **Administrator**
   - Manages users and oversees system operations.
   - Requires access to user management tools and system statistics.

4. **Auditor**
   - Monitors request processing and ensures compliance.
   - Needs access to detailed reports and request histories.

### Requirements

#### Functional Requirements
- **Authentication**: Secure login and registration for all user roles.
- **Request Submission**: Business customers can submit onboarding requests with necessary documents.
- **Request Processing**: CRM processors can review, approve, or reject requests.
- **User Management**: Administrators can create and manage user accounts.
- **Reporting**: Auditors can generate and view detailed reports.

#### Non-Functional Requirements
- **Security**: Ensure data protection through encryption and secure authentication.
- **Usability**: Provide an intuitive and user-friendly interface.
- **Performance**: Ensure the system can handle multiple concurrent users without performance degradation.
- **Scalability**: Design the system to accommodate future growth in user base and data volume.

### Wireframe Description for CRM Module Request Processing Screens

The CRM module's request processing screens will include:
- A **Dashboard** displaying a list of all requests with filters for status (All, Pending, Approved, Rejected).
- A **Request Detail View** where processors can see detailed information about each request, including uploaded documents and comments.
- A **Review Interface** with options to approve or reject requests, add comments, and update the request status.