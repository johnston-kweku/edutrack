# EduTrack - School Management System

EduTrack is a comprehensive School Management System built with Django and Tailwind CSS. It is designed to streamline academic administration, student tracking, and financial management for educational institutions.

## 🚀 Features

### 👤 User & Access Management
- **Role-Based Access Control**: Tailored experiences for Admins, Teaching Staff, and Parents.
- **Invitation System**: Secure, token-based invitation system for registering new users with specific roles.
- **Custom User Profiles**: Support for profile pictures, contact information, and professional titles.

### 📚 Academic Administration
- **Class Management**: Organize the school into Levels (KG, Primary, JHS) and Stages.
- **Subject Tracking**: Define subjects and assign them to specific classes and teachers.
- **Student Enrollment**: Automated Student ID generation and comprehensive student records.
- **Academic Calendar**: Manage academic years and terms.

### 📊 Performance & Attendance
- **Grading System**: Record and track student results (Class Scores and Exam Scores).
- **Attendance Tracking**: Daily attendance monitoring for students, marked by teaching staff.

### 💰 Finance Management
- **Fee Configuration**: Define fees per class and term.
- **Payment Tracking**: Record fee payments with automated balance calculations and payment history.

### 🖥️ Interactive Dashboards
- **Admin Dashboard**: Overview of school statistics and management tools.
- **Teacher Dashboard**: Access to class lists, attendance marking, and result entry.
- **Parent Dashboard**: Monitor student progress, attendance, and financial status.

## 🛠️ Tech Stack

- **Backend**: Django 6.x (Python)
- **Frontend**: Tailwind CSS 4.x, Vanilla JavaScript
- **Database**: SQLite (Default, configurable to PostgreSQL/MySQL)
- **Monitoring**: Sentry SDK
- **Styling**: Modern CSS with Tailwind CLI

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js & npm (for Tailwind CSS)

### 1. Clone the Repository
```bash
git clone https://github.com/johnston-kweku/edutrack.git
cd edutrack
```

### 2. Python Environment Setup
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
SENTRY_DSN=your-sentry-dsn
```

### 4. Database Migrations
```bash
python manage.py migrate
```

### 5. Tailwind CSS Setup
```bash
# Install Node dependencies
npm install

# Build styles
npm run build

# For development (watch mode)
npm run dev
```

### 6. Seed Data (Optional)
Populate the database with realistic Ghanaian sample data:
```bash
python manage.py populate_db
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## 📁 Project Structure

- `accounts/`: User authentication, roles, and invitations.
- `academics/`: Core logic for classes, subjects, students, results, and attendance.
- `finances/`: Fee management and payment tracking.
- `dashboards/`: Role-specific view logic and templates.
- `students/`: Student-specific utilities and views.
- `static/`: Global CSS and JavaScript assets.
- `templates/`: Global HTML templates (base, navbar, sidebar).

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the ISC License. See `package.json` for details.
