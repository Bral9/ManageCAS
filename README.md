# ManageCAS

## About

**Manage-CAS** is a lightweight Flask web app that helps schools run the IB CAS (Creativity, Activity, Service) workflow.  
Students write and organize their CAS reports, Teachers review and comment, and Admins manage accounts — all in a clean, OpenAI-inspired UI.

### Why it’s useful
- Centralizes CAS notes and feedback in one place (no email threads or scattered docs).
- Gives students a clear space to write, edit, and track their reflections.
- Lets teachers quickly browse students and leave comments.
- Requires almost no setup: runs on SQLite out of the box.

### Core features
- **Role-based access**: Student, Teacher, Admin
- **Notes CRUD** for students (create, edit, delete)
- **Teacher comments** on each note
- **Show all users** view for staff; assign classes
- **Authentication** with `flask-login`
- **SQLite + SQLAlchemy** (1-to-many: Student → Notes, Note → Comments)
- **Minimal, responsive UI** (OpenAI-style dark theme)
- **Optional rich text** via `Flask-CKEditor` (falls back to `<textarea>`)

### Tech stack
- Python (Flask 3.x), Jinja2 templates  
- SQLAlchemy ORM + SQLite  
- Flask-Login for auth  
- (Optional) Flask-CKEditor for rich text

### How it works (at a glance)
1. **Students** log in and write CAS notes (title + description).  
2. **Teachers/Admins** open a student’s notes and add comments.  
3. **Admins** can create teacher/student accounts and manage access.

> First run seeds a default Admin if none exists (email `brealtchuimi@gmail.com`, password `1234567`) — you can change it with `reset_admin.py`.
