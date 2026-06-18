# EduTrack - School Management System

EduTrack is a robust, enterprise-grade School Management System built with a **"System-First"** engineering philosophy. It prioritizes architectural integrity, scalability, and a high-fidelity user experience, leveraging the power of Django 6 and Tailwind CSS 4.

## 🏛️ Design Philosophy

- **System-First Architecture**: Every feature is designed with scalability and structural integrity in mind, ensuring that the backend logic is as resilient as the frontend is polished.
- **High-Fidelity UI/UX**: A modern, aesthetic-driven interface that avoids "default" styling. Every form, table, and dashboard is custom-crafted for clarity and professional flair.
- **Narrative Depth**: Documentation and code structure follow a logical narrative, making the system easy to maintain and evolve.

## 🚀 Features

### 🛡️ Security & Access Integrity
- **Decorator-Based RBAC**: Secure Role-Based Access Control enforced at the view level through custom, authenticated decorators.
- **Invitation System**: Secure, token-based invitation system for registering new users with specific roles, preventing unauthorized registration.
- **Secure Data Handling**: Robust input validation and sanitized logging to protect sensitive user credentials.

### 📚 Academic Administration
- **High-Fidelity Record Management**: Custom-built interfaces for enrolling and editing students and classes, featuring real-time validation feedback.
- **Intelligent Organization**: School structure organized into Levels (KG, Primary, JHS) and Stages with automated ID generation.
- **Subject & Teacher Mapping**: Dynamic assignment of subjects to classes and educators.

### 📊 Performance & Attendance
- **Integrated Grading**: Seamless tracking of Class and Exam scores with automated total calculations.
- **Daily Attendance**: Real-time attendance monitoring with historical tracking.

### 💰 Finance Management
- **Automated Fee Tracking**: Class-based fee configuration with automated balance calculations and payment histories.
- **Financial Transparency**: Real-time status updates for parents and admins regarding payment progress.

### 🖥️ Interactive Dashboards
- **Admin Command Center**: Holistic overview of school metrics and management tools.
- **Teacher Workspace**: Streamlined access to class lists, attendance, and grading.
- **Parent Portal**: Direct insight into student progress and financial status.

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
