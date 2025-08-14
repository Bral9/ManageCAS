from flask import Blueprint,render_template,request,redirect,flash,url_for
from . import *
from .models import Student, Teacher, Admin, Note, Comment
from flask_login import login_required, current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_ckeditor import CKEditorField
from . import db

views = Blueprint('views',__name__)

def getUserType():
    return current_user.__class__.__name__

userType = {
    'Student': Student,
    'Teacher': Teacher,
    'Admin': Admin,
}


@views.route('/comptes',methods=['GET','POST'])
@login_required

def comptes():
    if request.method=="POST":
        title=request.form['title']
        text=request.form['text']
        if title=="":
            flash("Pas de titre",category="error")
            return redirect(url_for('views.comptes'))
        
        elif len(text.split(" ")) < 100:
            flash("3000 caractères ou 500 mots au minimum",category="error")
            return redirect(url_for('views.comptes'))
        
        else:
            note = Note(title=title, text=text, student_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('views.comptes'))
            
    return render_template('comptes.html', note=None, user=current_user)
            
 
    
        
    #if getUserType() != "Student":
        #return redirect(url_for('views.accueil'))
    #else:
        #allTodo = Note.query.all()
        #return render_template("comptes.html",passallTodo = allTodo, user = current_user)


@views.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('views.comptes'))


@views.route('/update/<int:id>',methods=['GET', 'POST'])
@login_required
def updateNote(id):
    if request.method == 'POST':
        title=request.form.get('title')
        text=request.form.get('text')
        note = Note.query.filter_by(id=id).first()
        note.title=title
        note.text=text
        if title=="":
            flash("Aucun titre",category="error")
            return redirect(url_for('views.updateNote', id=note.id))
        elif len(text.split(" ")) < 5:
            flash("5 mots au minimum",category="error")
            return redirect(url_for('views.updateNote', id=note.id))

        else :
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('views.comptes'))

    note_update = Note.query.filter_by(id=id).first()
    return render_template("update.html",note=note_update,user=current_user)

@views.route('/',methods=['GET','POST'])
@login_required
def accueil():
    return render_template("accueil.html", user=current_user)
    

@views.route('/ressources-cas')
@login_required
def ressources():
    return render_template("ressources.html", user = current_user) 

@views.route("/all-users",methods=['GET','POST'])
@login_required
def allStudents():
    all_students=Student.query.all()
    var=[]
    for student in all_students:
        notes=Note.query.filter_by(student_id=student.id).all()
        if len(notes)>0:
            var.append(len(notes))
        else:
            var.append(0)
    
    if request.method=="POST":
        classe = request.form.get('classe')
        studid = request.form.get('studid')
        print(classe)
        student = Student.query.filter_by(id=studid).first()
        student.classe = classe
        db.session.commit()

    if getUserType() not in  ("Admin", "Teacher"):
        return redirect(url_for('views.accueil'))
    else:
        return render_template("showusers.html",all_users=zip(all_students,var),user=current_user)



@views.route("/details/<int:id>",methods=['GET','POST'])   
@login_required
def details(id):
    return render_template("details.html",user=current_user)



@views.route("/deleteAcc/<int:id>",methods=['GET','POST']) #La route récupère l'id de l'utilisateur
@login_required
#La méthode deleteACC récupère l'id de l'utilisateur qui souhaite supprimer son compte
def deleteACC(id):
    #On récupère le type d'utilisateur (Elève, Administrateur, ou Professeur)
    user = userType[getUserType()].query.filter_by(id=id).first()
    if user:
        #On supprime l'utilisateur, et on le déconnecte de la plateforme
        db.session.delete(user)
        db.session.commit()
        logout_user()

        flash("Compte supprimé avec succès !",category="success")

        #On redirige l'utilisateur vers la page de connexion
        return redirect(url_for('auth.login'))

@views.route("/usernotes/<int:id>",methods=['GET','POST'])
@login_required
#création d'une fonction usernotes qui permet de commenter le compte rendu de l'élève
#cette fonction récupère l'id de l'élève
def usernotes(id):
    #cette commande recherche dan la base de données l'enregistrement de l'élève avec l'id donné
    student = Student.query.filter_by(id=id).first()
    if request.method=="POST":
        #récupérer l'id du compte rendu, et créer le commentaire du professeur 
        #dans la base de données
        getid=request.form['getId']
        desc=request.form[f'desc{getid}']
        comment=Comment(text=desc, note_id=getid)
        db.session.add(comment)
        db.session.commit()
        flash("Commentaire ajouté avec succès",category="success")        
    #montrer la template usernotes.html, en passant l'objet student et le current_user
    return render_template("usernotes.html",student=student, user=current_user)


        

@views.route("/see-comments/<int:id>",methods=['GET','POST'])
@login_required
def teacher_comments(id):
    note = Note.query.filter_by(id=id).first()
    return render_template("teacher_comments.html",note=note, user=current_user)













