from flask_login import UserMixin
from db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Register(UserMixin, db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Register {self.username}>'
    
class AcadamicYear(db.Model):
    __tablename__ = 'acadamic_years'

    id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<AcadamicYear {self.year_name}>'
class Departments(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Department {self.department_name}>'
class Standards(db.Model):
    __tablename__ = 'standards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Standards {self.name}>'
class Roles(db.Model):
    __tablename__="roles"
    
    id=db.Column(db.Integer , primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f'<Roles {self.name}>'
    


class Students(UserMixin, db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    acadamic_year_id = db.Column(db.Integer, db.ForeignKey('acadamic_years.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    standard_id = db.Column(db.Integer, db.ForeignKey('standards.id'), nullable=False)

    acadamic_year = db.relationship('AcadamicYear', backref='students')
    department = db.relationship('Departments', backref='students')
    standard = db.relationship('Standards', backref='students')

    def __repr__(self):
        return f'<Student {self.name}>'