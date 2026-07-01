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

## ⚙️ App Documentation

This section provides a detailed overview of each Django app within the EduTrack project.

### 1. `accounts` App
   - **Purpose**: Manages user authentication, authorization, roles, and the invitation system.
   - **Key Models**:
     - `User`: Extends Django's built-in User model to include `full_name`, `title`, `role` (Admin, Teaching Staff, Parent), `contact`, and `picture`.
     - `Invitation`: Handles secure, token-based invitations for new user registrations, specifying role and expiry.
   - **Key Features**:
     - Role-Based Access Control (RBAC) via `role_required` decorator.
     - Secure user registration through invitations.
     - User profile management.

### 2. `academics` App
   - **Purpose**: Core application for managing academic structures, students, subjects, terms, and attendance.
   - **Key Models**:
     - `Class`: Represents academic classes with stages and levels (KG, Primary, JHS), and an optional `class_teacher`. Includes validation for valid stage/level combinations.
     - `Subject`: Defines academic subjects.
     - `ClassSubject`: Maps subjects to specific classes and assigns a `teacher`.
     - `AcademicYear`: Manages academic years, including tracking the current year.
     - `Term`: Manages academic terms within an academic year, including tracking the current term.
     - `Student`: Stores student information, including ID generation, personal details, parent linkage, and an optional profile image (with image compression).
     - `Assessment`: Defines different types of assessments (Quiz, Class Test, Exam, Exercise) with associated scores, subjects, terms, and classes.
     - `AssessmentRecord`: Records individual student scores for specific assessments, with validation against `max_score`.
     - `Attendance`: Tracks daily attendance for a class, marked by a staff member.
     - `AttendanceRecord`: Records the presence or absence of individual students for a given attendance entry.
   - **Key Features**:
     - Hierarchical class structure.
     - Automated student ID generation.
     - Comprehensive academic year and term management.
     - Robust assessment and grading system.
     - Daily attendance tracking.
     - Image handling for student profiles with compression.

### 3. `finances` App
   - **Purpose**: Handles financial aspects of the school, specifically fee management and payments.
   - **Key Models**:
     - `Fee`: Defines fees for specific classes and terms, including amount and description. Ensures unique fee configurations per class/term.
     - `FeePayment`: Records student payments towards fees, calculating `amount_tendered`, `balance`, and tracking who received the payment. Automatically calculates balance based on previous payments.
   - **Key Features**:
     - Class and term-specific fee configuration.
     - Automated calculation of outstanding balances.
     - Payment history tracking.

### 4. `dashboards` App
   - **Purpose**: Provides role-specific dashboards for different user types (Admin, Teacher, Parent).
   - **Key Models**: (Likely minimal models, primarily focused on views/templates)
   - **Key Features**:
     - Centralized overview for administrators.
     - Workspace for teachers to manage classes and students.
     - Parent portal for tracking student progress and finances.

### 5. `students` App
   - **Purpose**: Contains student-specific utilities, views, or additional models not covered by `academics`.
   - **Key Models**: (Based on provided `students/models.py`, it's currently empty, suggesting its purpose might evolve or be integrated elsewhere.)
   - **Key Features**: (To be defined as the app grows)

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
