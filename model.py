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
    
class Division(db.Model):
    __tablename__ = "division"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Division {self.name}>"
class Faculty_Department(db.Model):
    __tablename__ = 'faculty_department'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f"<Faculty_Department {self.name}>"
class Subjects(db.Model):
    __tablename__='subjects'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f'<Subjects {self.name}>'
class Medium(db.Model):
    __tablename__="Medium"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f'<Subjects {self.name}>'
    
class Faculty(db.Model):
    __tablename__='faculty'
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    fmid=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    phone=db.Column(db.String(15),nullable=False)
    gender=db.Column(db.String(10),nullable=False)
    address=db.Column(db.String(250),nullable=False)
    city=db.Column(db.String(100),nullable=False)
    state=db.Column(db.String(100),nullable=False)
    pincode=db.Column(db.String(10),nullable=False)
    date_of_birth=db.Column(db.Date,nullable=False)
    joining_date=db.Column(db.Date,nullable=False)
    qualification=db.Column(db.String(150),nullable=False)
    experience=db.Column(db.String(100),nullable=False)
    faculty_department_id=db.Column(db.Integer,db.ForeignKey('faculty_department.id'),nullable=False)
    
    Faculty_Department=db.relationship('Faculty_Department',backref='faculty')
    def __repr__(self):
        return f'<Faculty{self.name}>'

class Students(UserMixin, db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_number = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_of_addmission = db.Column(db.Date, nullable=True)
    gender= db.Column(db.String(10), nullable=True)
    nationality=db.Column(db.String(50),nullable=True)
    religion=db.Column(db.String(50),nullable=True)
    category=db.Column(db.String(50),nullable=True)
    father_name=db.Column(db.String(150),nullable=True)
    mother_name=db.Column(db.String(150),nullable=True)
    
    acadamic_year_id = db.Column(db.Integer, db.ForeignKey('acadamic_years.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    standard_id = db.Column(db.Integer, db.ForeignKey('standards.id'), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey('Medium.id'), nullable=False)


    acadamic_year = db.relationship('AcadamicYear', backref='students')
    department = db.relationship('Departments', backref='students')
    standard = db.relationship('Standards', backref='students')
    division=db.relationship('Division', backref='students')
    Medium=db.relationship('Medium',backref='students')

    def __repr__(self):
        return f'<Student {self.name}>'