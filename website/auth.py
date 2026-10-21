from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import os
import secrets

from werkzeug.security import generate_password_hash, check_password_hash
from .database import db                      
from .models import Student, Teacher, Admin   

auth = Blueprint('auth', __name__)

def getUserType():
    return current_user.__class__.__name__

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # First admin comes from the environment, never from the code
    seed_email, seed_password = os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD')
    if seed_email and seed_password and not Admin.query.filter_by(email=seed_email).first():
        db.session.add(Admin(
            email=seed_email,
            password=generate_password_hash(seed_password),
            first_name='Admin'
        ))
        db.session.commit()

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''

        if not email or not password:
            flash('Veuillez remplir votre email et votre mot de passe.', 'error')
            return render_template("login.html", user=current_user)

        # ✅ Prefer Admin → Teacher → Student to avoid picking the wrong class
        user = (Admin.query.filter_by(email=email).first()
                or Teacher.query.filter_by(email=email).first()
                or Student.query.filter_by(email=email).first())

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash(f'Connecté en tant que {user.__class__.__name__}', 'success')
            return redirect(url_for('views.accueil'))
        else:
            flash('Identifiants invalides.', 'error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/add-user', methods=['GET','POST'])
@login_required
def add_user():
    # ✅ Only Admin may access
    if getUserType() != "Admin":
        return redirect(url_for('views.accueil'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        first_name = (request.form.get('firstName') or '').strip()
        teacher = request.form.get('teacher')  # checkbox or value
        password = secrets.token_urlsafe(9)  # shown once to the admin below

        # Avoid duplicates across all tables
        exists = (Student.query.filter_by(email=email).first()
                  or Teacher.query.filter_by(email=email).first()
                  or Admin.query.filter_by(email=email).first())

        if exists:
            flash("L'email existe déjà.", 'error')
        elif len(first_name) < 2:
            flash('Le prénom doit être supérieur à 1 caractère.', 'error')
        else:
            user = (Teacher(email=email, first_name=first_name,
                            password=generate_password_hash(password))
                    if teacher else
                    Student(email=email, first_name=first_name,
                            password=generate_password_hash(password)))
            db.session.add(user)
            db.session.commit()
            flash(f'Le compte a été créé avec succès. Mot de passe temporaire : {password}', 'success')

    return render_template("add_user.html", user=current_user)

@auth.route('/changePass/<int:id>', methods=['POST'])
@login_required
def changePass(id):
    # Users may only change their own password
    if id != current_user.id:
        flash("Action non autorisée.", 'error')
        return redirect(url_for("views.details", id=current_user.id))

    password1 = request.form.get('password1') or ''
    password2 = request.form.get('password2') or ''

    if password1 != password2:
        flash('Passwords does not match.', 'error')
        return render_template("details.html", user=current_user)

    mapping = {'Student': Student, 'Teacher': Teacher, 'Admin': Admin}
    model = mapping.get(getUserType())
    user = model.query.filter_by(id=id).first() if model else None

    if not user:
        flash("Utilisateur introuvable.", 'error')
        return redirect(url_for("views.details", id=current_user.id))

    user.password = generate_password_hash(password1)
    db.session.commit()
    flash("Le mot de passe a été changé avec succès", 'success')
    return redirect(url_for("views.details", id=current_user.id))
