from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)  # Only for admin users
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)  # WhatsApp phone number
    user_type = db.Column(db.String(20), nullable=False)  # 'professor', 'student', or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    professor = db.relationship('User', backref='courses_taught')

class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='enrolled_courses')
    course = db.relationship('Course', backref='enrolled_students')

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    homework_grade = db.Column(db.Float, default=0.0)  # 30%
    exam_grade = db.Column(db.Float, default=0.0)      # 70%
    total_grade = db.Column(db.Float, default=0.0)     # Calculated automatically
    status = db.Column(db.String(20), default='En reprise')  # 'Réussi' or 'En reprise'
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = db.relationship('User', backref='grades')
    course = db.relationship('Course', backref='grades')
    
    def calculate_total_grade(self):
        """Calcule la note totale et détermine le statut"""
        self.total_grade = (self.homework_grade * 0.3) + (self.exam_grade * 0.7)
        self.status = 'Réussi' if self.total_grade >= 80.0 else 'En reprise'