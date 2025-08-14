from .database import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_ckeditor import CKEditorField



class Note(db.Model):
    #C'est une base de données relationnelle qui permet une relation de un à 
    # plusieurs entre les comptes rendus de élèves et les commentaires 
    # des professeurs.
    # Un compte rendu peut avoir plusieurs commentaires, mais un commentaire est
    # forcément assigné à un compte rendu

    
    title = db.Column(db.String(100))
    text = db.Column(db.String())
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    comment = db.relationship('Comment')

    # student_id est une clé étrangère de la table Note et fait référence 
    # à student.id qui
    # est l'idée de l'élève. id est la clé primaire dans la table Note.
    id = db.Column(db.Integer, primary_key = True, unique = True)
    student_id = db.Column(db.Integer,db.ForeignKey("student.id"))




class Student(db.Model, UserMixin):

    #C'est une base de données relationnelle qui permet une relation de un à 
    # plusieurs entre les élèves et les comptes rendus.
    # Un élève peut avoir plusieurs comptes rendus, mais un compte rendu
    # a été rédigé par un élève 

    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    classe = db.Column(db.String(150))
    #id est la clé primaire de la table Student
    id = db.Column(db.Integer, primary_key = True, unique = True)
    def get_id(self):
        # retourne l'email de l'utilisateur
        return str(self.email)


class Teacher(db.Model, UserMixin):
    #L'id est la clé primaire de la table Teacher
    id = db.Column(db.Integer, primary_key = True, unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(150))
    def get_id(self):
     # retourne l'email de l'utilisateur
        return str(self.email)

class Comment(db.Model, UserMixin) :
    #L'id est la clé primaire de la table Comment
    id = db.Column(db.Integer, primary_key = True, unique = True)

    text = db.Column(db.String(5000))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    note_id = db.Column(db.Integer,db.ForeignKey("note.id"))


class Admin(db.Model, UserMixin):
    #L'id est la clé primaire de la table Teacher
    id = db.Column(db.Integer, primary_key = True, unique = True)

    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(150))
    def get_id(self):
        # retourne l'email de l'utilisateur
        return str(self.email)

        