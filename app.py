from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Course, StudentCourse, Grade
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'academic_megd_haiti_secret_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Données initiales pour peupler la base
def create_sample_data():
    # Vérifier si des données existent déjà
    if User.query.first() is None:
        # Créer l'administrateur
        admin = User(
            username='Stan',
            password='StanEcoleBibliqueMegdHaiti1986',
            full_name='Administrateur Stan',
            phone_number='+243900000000',
            user_type='admin'
        )
        db.session.add(admin)
        
        # Créer des professeurs
        prof1 = User(username='prof.dupont', full_name='Professeure Marie Dupont', phone_number='+243900000001', user_type='professor')
        prof2 = User(username='prof.martin', full_name='Professeur Jean Martin', phone_number='+243900000002', user_type='professor')
        
        # Créer des étudiants
        students = [
            User(username='etudiant.leroy', full_name='Étudiant Pierre Leroy', phone_number='+243900000003', user_type='student'),
            User(username='etudiant.bernard', full_name='Étudiante Sophie Bernard', phone_number='+243900000004', user_type='student'),
            User(username='etudiant.moreau', full_name='Étudiant Thomas Moreau', phone_number='+243900000005', user_type='student'),
            User(username='etudiant.petit', full_name='Étudiante Claire Petit', phone_number='+243900000006', user_type='student')
        ]
        
        db.session.add(prof1)
        db.session.add(prof2)
        for student in students:
            db.session.add(student)
        
        db.session.commit()
        
        # Créer des cours
        course1 = Course(title='Mathématiques Avancées', professor_id=prof1.id)
        course2 = Course(title='Programmation Python', professor_id=prof2.id)
        course3 = Course(title='Base de Données', professor_id=prof1.id)
        
        db.session.add(course1)
        db.session.add(course2)
        db.session.add(course3)
        db.session.commit()
        
        # Assigner des étudiants aux cours
        all_students = User.query.filter_by(user_type='student').all()
        all_courses = Course.query.all()
        
        for student in all_students:
            for course in all_courses:
                enrollment = StudentCourse(student_id=student.id, course_id=course.id)
                db.session.add(enrollment)
        
        db.session.commit()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username:
            flash('Identifiant obligatoire.', 'error')
            return redirect(url_for('login'))
        
        # Check if this is an admin login
        if username == 'Stan':
            if not password:
                flash('Mot de passe requis pour l\'administrateur.', 'error')
                return redirect(url_for('login'))
            
            user = User.query.filter_by(username=username, password=password).first()
            
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                session['full_name'] = user.full_name
                session['user_type'] = user.user_type
                
                flash(f'Bienvenue {user.full_name}!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        else:
            # Regular user login (professor or student)
            user = User.query.filter_by(username=username).first()
            
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                session['full_name'] = user.full_name
                session['user_type'] = user.user_type
                
                flash(f'Bienvenue {user.full_name}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Identifiant non trouvé.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        user_type = request.form.get('user_type', '').strip()
        
        # Validation
        if not full_name or not phone_number or not user_type:
            flash('Tous les champs sont obligatoires.', 'error')
            return redirect(url_for('register'))
        
        if user_type not in ['professor', 'student']:
            flash('Type d\'utilisateur invalide.', 'error')
            return redirect(url_for('register'))
        
        # Vérifier si le numéro de téléphone existe déjà
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            flash('Ce numéro WhatsApp est déjà enregistré.', 'error')
            return redirect(url_for('register'))
        
        # Générer un nom d'utilisateur unique à partir du nom complet
        # Convertir "Jean Dupont" en "jean.dupont"
        username_base = full_name.lower().replace(' ', '.')
        username_base = ''.join(c for c in username_base if c.isalnum() or c == '.')
        
        # Vérifier l'unicité et ajouter un numéro si nécessaire
        username = username_base
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{username_base}{counter}"
            counter += 1
        
        # Créer le nouvel utilisateur
        new_user = User(
            username=username,
            full_name=full_name,
            phone_number=phone_number,
            user_type=user_type
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Connexion automatique après inscription
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['full_name'] = new_user.full_name
        session['user_type'] = new_user.user_type
        
        flash(f'Inscription réussie! Bienvenue {new_user.full_name}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'admin':
        flash('Accès réservé aux administrateurs.', 'error')
        return redirect(url_for('login'))
    
    # Statistiques globales
    total_users = User.query.count()
    total_professors = User.query.filter_by(user_type='professor').count()
    total_students = User.query.filter_by(user_type='student').count()
    total_courses = Course.query.count()
    total_grades = Grade.query.count()
    
    # Récupérer tous les utilisateurs
    all_users = User.query.all()
    all_courses = Course.query.all()
    
    # Statistiques des notes
    passing_students = Grade.query.filter_by(status='Réussi').count()
    failing_students = Grade.query.filter_by(status='En reprise').count()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_professors=total_professors,
                         total_students=total_students,
                         total_courses=total_courses,
                         total_grades=total_grades,
                         passing_students=passing_students,
                         failing_students=failing_students,
                         all_users=all_users,
                         all_courses=all_courses)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Redirect admin to admin dashboard
    if user.user_type == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    if user.user_type == 'professor':
        # Pour les professeurs: leurs cours et statistiques
        courses = Course.query.filter_by(professor_id=user.id).all()
        total_students = 0
        for course in courses:
            total_students += len(course.enrolled_students)
        
        return render_template('dashboard.html', 
                             user=user, 
                             courses=courses, 
                             total_students=total_students)
    
    else:  # Étudiant
        # Pour les étudiants: leurs notes et statuts
        enrollments = StudentCourse.query.filter_by(student_id=user.id).all()
        grades_data = []
        
        for enrollment in enrollments:
            grade = Grade.query.filter_by(
                student_id=user.id, 
                course_id=enrollment.course_id
            ).first()
            
            if grade:
                grades_data.append({
                    'course': enrollment.course,
                    'homework_grade': grade.homework_grade,
                    'exam_grade': grade.exam_grade,
                    'total_grade': grade.total_grade,
                    'status': grade.status
                })
            else:
                grades_data.append({
                    'course': enrollment.course,
                    'homework_grade': 'Non noté',
                    'exam_grade': 'Non noté',
                    'total_grade': 'Non noté',
                    'status': 'En attente'
                })
        
        return render_template('student_grades.html', 
                             user=user, 
                             grades_data=grades_data)

@app.route('/manage_courses', methods=['GET', 'POST'])
def manage_courses():
    if 'user_id' not in session or session['user_type'] != 'professor':
        flash('Accès réservé aux professeurs.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        
        if not title:
            flash('Titre du cours obligatoire.', 'error')
            return redirect(url_for('manage_courses'))
        
        # Créer le nouveau cours
        new_course = Course(
            title=title,
            professor_id=session['user_id']
        )
        
        db.session.add(new_course)
        db.session.commit()
        
        # Assigner tous les étudiants au nouveau cours
        students = User.query.filter_by(user_type='student').all()
        for student in students:
            enrollment = StudentCourse(
                student_id=student.id,
                course_id=new_course.id
            )
            db.session.add(enrollment)
        
        db.session.commit()
        
        flash(f'Cours "{title}" créé avec succès!', 'success')
        return redirect(url_for('manage_courses'))
    
    # GET: Afficher les cours du professeur
    courses = Course.query.filter_by(professor_id=session['user_id']).all()
    return render_template('manage_courses.html', courses=courses)

@app.route('/manage_grades/<int:course_id>', methods=['GET', 'POST'])
def manage_grades(course_id):
    if 'user_id' not in session or session['user_type'] != 'professor':
        flash('Accès réservé aux professeurs.', 'error')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    
    # Vérifier que le cours appartient au professeur connecté
    if course.professor_id != session['user_id']:
        flash('Accès non autorisé à ce cours.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        homework_grade = request.form.get('homework_grade', '0')
        exam_grade = request.form.get('exam_grade', '0')
        
        try:
            homework_grade = float(homework_grade)
            exam_grade = float(exam_grade)
            
            if homework_grade < 0 or homework_grade > 100 or exam_grade < 0 or exam_grade > 100:
                raise ValueError("Les notes doivent être entre 0 et 100")
            
        except ValueError:
            flash('Notes invalides. Utilisez des nombres entre 0 et 100.', 'error')
            return redirect(url_for('manage_grades', course_id=course_id))
        
        # Chercher ou créer l'entrée de notes
        grade = Grade.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
        
        if not grade:
            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                homework_grade=homework_grade,
                exam_grade=exam_grade
            )
            db.session.add(grade)
        else:
            grade.homework_grade = homework_grade
            grade.exam_grade = exam_grade
        
        # Calculer la note totale et le statut
        grade.calculate_total_grade()
        db.session.commit()
        
        flash('Notes mises à jour avec succès!', 'success')
        return redirect(url_for('manage_grades', course_id=course_id))
    
    # GET: Afficher les étudiants et leurs notes
    enrollments = StudentCourse.query.filter_by(course_id=course_id).all()
    students_grades = []
    
    for enrollment in enrollments:
        grade = Grade.query.filter_by(
            student_id=enrollment.student_id,
            course_id=course_id
        ).first()
        
        students_grades.append({
            'student': enrollment.student,
            'homework_grade': grade.homework_grade if grade else 0,
            'exam_grade': grade.exam_grade if grade else 0,
            'total_grade': grade.total_grade if grade else 0,
            'status': grade.status if grade else 'En attente'
        })
    
    return render_template('manage_grades.html', 
                         course=course, 
                         students_grades=students_grades)

@app.route('/whatsapp_alerts')
def whatsapp_alerts():
    if 'user_id' not in session or session['user_type'] != 'professor':
        flash('Accès réservé aux professeurs.', 'error')
        return redirect(url_for('dashboard'))
    
    # Récupérer tous les étudiants avec leurs notes
    students = User.query.filter_by(user_type='student').all()
    alerts_data = []
    
    for student in students:
        grades = Grade.query.filter_by(student_id=student.id).all()
        student_courses = []
        
        for grade in grades:
            course = Course.query.get(grade.course_id)
            student_courses.append({
                'course': course,
                'total_grade': grade.total_grade,
                'status': grade.status
            })
        
        if student_courses:
            alerts_data.append({
                'student': student,
                'courses': student_courses
            })
    
    return render_template('whatsapp_alerts.html', alerts_data=alerts_data)

@app.route('/api/student_grades/<int:student_id>')
def api_student_grades(student_id):
    """API pour récupérer les notes d'un étudiant"""
    if 'user_id' not in session:
        return jsonify({'error': 'Non authentifié'}), 401
    
    student = User.query.get_or_404(student_id)
    grades = Grade.query.filter_by(student_id=student_id).all()
    
    grades_data = []
    for grade in grades:
        course = Course.query.get(grade.course_id)
        grades_data.append({
            'course_title': course.title,
            'homework_grade': grade.homework_grade,
            'exam_grade': grade.exam_grade,
            'total_grade': grade.total_grade,
            'status': grade.status
        })
    
    return jsonify({
        'student_name': student.full_name,
        'grades': grades_data
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)