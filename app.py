from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db import db
import csv
import pymysql
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from model import Register, AcadamicYear, Departments, Standards , Roles , Division , Students , Faculty_Department , Faculty , Medium
from flask_mail import Message, Mail
from flask_migrate import Migrate
import pandas as pd
from flask import send_file
import io

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Mail Config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    
    mail = Mail(app)
    db.init_app(app)
    # migrate = Migrate(app, db)

    with app.app_context():
        from model import User, Register
        db.create_all()
        print("Tables created!")

    # ---------------- ROUTES ---------------- #

    @app.route('/')
    def landing():
        return render_template('landing.html')

    @app.route('/register')
    def register_page():
        return render_template('Register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
    
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='R@j@t2004',
                database='Student_M1'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM register WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            
            if user_data and user_data[3] == password:
                session['username'] = user_data[1]
                flash("Login successful!", "login_success")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password!", "login_error")
                return render_template('login.html')
        
        return render_template('login.html')

    @app.route('/login.html')
    def login2():
        return render_template('login.html')

    @app.route('/feature')
    def feature():
        return render_template('feature.html')

    @app.route('/Register.html', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form['role']

            if password != confirm_password:
                flash("Passwords do not match!", "danger")
                return redirect('/Register.html')

            existing_user = Register.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists!", "warning")
                return redirect('/Register.html')

            new_user = Register(username=username, email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect('/login')

        return render_template('Register.html')

    @app.route('/home')
    def home():
        if 'username' in session:
            return render_template('home.html', username=session['username'])
        else:
            flash("You need to log in first!", "danger")
            return redirect(url_for('login'))

    @app.route('/about/')
    def about():
        return render_template('about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            message = request.form["message"]

            msg = Message(
                subject=f"📥 Feedback from {name}",
                sender=email,
                recipients=["rajatpurohit@gmail.com"],  # 👈 Replace with your actual email
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Thank you for your feedback!", "success")
            return redirect(url_for("contact"))

        return render_template("contact.html")

    @app.route('/logout')
    def logout():
        session.clear()
        # flash("Logged out successfully.", "info")
        return redirect(url_for('landing'))

    # -------- Departments -------- #
    @app.route('/department', methods=['GET', 'POST'])
    def department():
        if request.method == 'POST':
            dept_name = request.form.get('department_name')
            if dept_name:
                existing = Departments.query.filter_by(department_name=dept_name).first()
                if existing:
                    flash("Department already exists!", "error")
                else:
                    new_dept = Departments(department_name=dept_name)
                    try:
                        db.session.add(new_dept)
                        db.session.commit()
                        flash("Department added successfully!", "success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding department: {str(e)}", "error")
                return redirect(url_for('department'))
        departments_list = Departments.query.all()
        return render_template('department.html', departments=departments_list)

    @app.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
    def edit_department(id):
        new_dept = request.form.get('department_name')
        dept = Departments.query.get_or_404(id)
        dept.department_name = new_dept
        db.session.commit()
        flash("Department updated successfully!", "success")
        return redirect(url_for('department'))

    @app.route('/departments/delete/<int:id>', methods=['POST','GET'])
    def delete_department(id):
        dept = Departments.query.get_or_404(id)
        if dept.students:
            flash("Cannot delete department Because students exist for this department.", "deletedepterror")
            return redirect(url_for('department'))
        db.session.delete(dept)
        db.session.commit()
        flash("Department deleted successfully!", "success")
        return redirect(url_for('department'))

    # -------- Academic Year -------- #
    @app.route('/acadamic_year', methods=['GET', 'POST'])
    def acadamic_year():
        if request.method == 'POST':
            year = request.form.get('acadamic_year')
            if year:
                existing = AcadamicYear.query.filter_by(year_name=year).first()
                if existing:
                    flash("Academic year already exists!", "year_error")
                else:
                    new_year = AcadamicYear(year_name=year)
                    try:
                        db.session.add(new_year)
                        db.session.commit()
                        flash("Academic year added successfully!", "year_success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding academic year: {str(e)}", "year_error")
                return redirect(url_for('acadamic_year'))
        years = AcadamicYear.query.all()
        return render_template("acadamic_year.html", years=years)

    @app.route('/acadamic_years/edit/<int:id>', methods=['GET', 'POST'])
    def edit_acadamic_year(id):
        new_year = request.form.get('year_name')
        ay = AcadamicYear.query.get_or_404(id)
        ay.year_name = new_year
        db.session.commit()
        flash("Academic year updated successfully!", "year_success")
        return redirect(url_for('acadamic_year'))

    @app.route('/acadamic_years/delete/<int:id>', methods=['POST','GET'])
    def delete_acadamic_year(id):
        ay = AcadamicYear.query.get_or_404(id)
        if ay.students:
            flash("Cannot delete academic year Because students exist for this year.", "year_error")
            return redirect(url_for('acadamic_year'))
        db.session.delete(ay)
        db.session.commit()
        flash("Academic year deleted successfully!", "year_success")
        return redirect(url_for('acadamic_year'))

    # -------- Standards -------- #
    @app.route('/Standards', methods=['GET','POST'])
    def standards_page():
        if request.method == 'POST':
            year = request.form.get('standard_name')
            if year:
                existing = Standards.query.filter_by(name=year).first()
                if existing:
                    flash("Standard already exists", "error")
                else:
                    new_standard = Standards(name=year)
                    try:
                        db.session.add(new_standard)
                        db.session.commit()
                        flash("Standard added successfully", "success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding standard: {str(e)}", "error")
            return redirect(url_for('standards_page'))

        all_standards = Standards.query.all()
        return render_template('Standards.html', standards=all_standards)

    @app.route('/standards/edit/<int:id>', methods=['GET', 'POST'])
    def edit_standards(id):
        st = Standards.query.get_or_404(id)
        if request.method == 'POST':
            new_standard = request.form.get('standards')
            st.name = new_standard
            db.session.commit()
            flash("Standard updated successfully!", "success")
            return redirect(url_for('standards_page'))

    @app.route('/standards/delete/<int:id>', methods=['POST','GET'])
    def delete_standards(id):
        st = Standards.query.get_or_404(id)
        if st.students:
            flash("Cannot delete standard Because students exist for this standard.", "deletestandarderror")
            return redirect(url_for('standards_page'))
        db.session.delete(st)
        db.session.commit()
        flash("Standard deleted successfully!", "success")
        return redirect(url_for('standards_page'))
    @app.route('/Roles',methods=['GET','Post'])
    def roles_page():
        if request.method =='POST':
            role_name=request.form.get('Roles')
            if role_name:
                existing=Roles.query.filter_by(name=role_name).first()
                if existing:
                    flash("Role already exists","error")
                else:
                    new_role=Roles(name=role_name)
                    try:
                        db.session.add(new_role)
                        db.session.commit()
                        flash("Role added successfully","success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding role: {str(e)}","error")
            return redirect(url_for('roles_page'))
        all_roles=Roles.query.all()
        return render_template('Roles.html',Roles=all_roles)
    @app.route('/Roles/edit/<int:id>',methods=['GET','POST'])
    def Edit_Roles(id):
        role=Roles.query.get_or_404(id)
        if request.method=='POST':
            new_role=request.form.get('Roles_name')
            role.name=new_role
            db.session.commit()
            flash("Role updated successfully!","success")
            return redirect(url_for('roles_page'))
    @app.route('/Roles/delete/<int:id>',methods=['POST','GET'])
    def Delete_Roles(id):
        role=Roles.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        flash("Role deleted successfully!","success")
        return redirect(url_for('roles_page'))
    @app.route('/division', methods=['GET', 'POST'])
    def Division_page():
        if request.method=="POST":
            division_name=request.form.get('Division')
            if division_name:
                existing=Division.query.filter_by(name=division_name).first()
                if existing:
                    flash("Role already exists", "error")
                else:
                    new_division=Division(name=division_name)
                    try:
                        db.session.add(new_division)
                        db.session.commit()
                        flash("Division added successfully","successdivision")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding Division: {str(e)}","errordivision")
            return redirect(url_for('Division_page'))
        all_division=Division.query.all()
        return render_template('division.html',Division=all_division)
    @app.route('/Division/edit/<int:id>',methods=['GET','POST'])
    def Edit_Division(id):
        division=Division.query.get_or_404(id)
        if request.method=='POST':
            new_division=request.form.get('Division_name')
            division.name=new_division
            db.session.commit()
            flash("Division updated successfully!","successdivision")
            return redirect(url_for('Division_page'))
    @app.route('/Division/delete/<int:id>',methods=['POST','GET'])
    def Delete_Division(id):
        division=Division.query.get_or_404(id)
        if division.students:
            flash("Cannot delete Division Because students already exist for this Division.","deletedivisionerror")
            return redirect(url_for('Division_page'))
        db.session.delete(division)
        db.session.commit()
        flash("Division deleted successfully!","successdivision")
        return redirect(url_for('Division_page'))
    @app.route('/Add_student', methods=['GET', 'POST'])
    def Add_student():
        if request.method == 'POST':
            try:
                name=request.form.get('name')
                enrollment_number=request.form.get('enrollment_number')
                email=request.form.get('email')
                phone=request.form.get('phone')
                address=request.form.get('address')
                date_of_birth=request.form.get('dob')
                date_of_addmission=request.form.get('doa')
                gender=request.form.get('gender')
                father_name=request.form.get('father_name')
                mother_name=request.form.get('mother_name')
                nationality=request.form.get('nationality')
                religion=request.form.get('religion')
                category=request.form.get('category')
                
                
                acadamic_year_id=request.form.get('academic_year')
                department_id=request.form.get('department_id')
                standard_id=request.form.get('standard_id')
                division_id=request.form.get('division_id')
                
                existing_student = Students.query.filter_by(email=email).first()
                if existing_student:
                    flash("Error: Student with this email already exists!", "Emailerror")
                    return redirect(url_for('Add_student'))
                
                new_student=Students(
                    name=name,
                    enrollment_number=enrollment_number,
                    email=email,
                    phone=phone,
                    address=address,
                    date_of_birth=date_of_birth,
                    date_of_addmission=date_of_addmission,
                    gender=gender,
                    father_name=father_name,
                    mother_name=mother_name,
                    nationality=nationality,
                    religion=religion,
                    category=category,
                    acadamic_year_id=acadamic_year_id,
                    department_id=department_id,
                    standard_id=standard_id,
                    division_id=division_id
                )
                if not acadamic_year_id or not department_id or not standard_id or not division_id:
                    flash("Error: All dropdowns must be selected!", "dropdownerror")
                    return redirect(url_for('Add_student'))
                db.session.add(new_student)
                db.session.commit()
                flash("Student added successfully!","addsuccess")
                return redirect(url_for('Add_student'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding student: {str(e)}", "adderror")
                return redirect(url_for('Add_student'))
        
        
        #send dropdown data to template
        years=AcadamicYear.query.all()
        departments=Departments.query.all()
        standards=Standards.query.all()
        divisions=Division.query.all()
        
        return render_template(
            'addstudent.html',
            years=years,
            departments=departments,
            standards=standards,
            divisions=divisions     
        )
    @app.route('/Add_bulk_student')
    def Add_bulk_student():
        return render_template('addbulkstudent.html')
    @app.route('/download_sample_excel')
    def download_sample_excel():
        # Required student columns
        student_columns = ["name","enrollment number", "email", "phone", "address", "date_of_birth","date_of_addmission",
                           "gender", "father_name", "mother_name", "nationality", "religion", "category",
                        "acadamic_year", "department", "standard", "division"]

        # Blank student sheet
        df_students = pd.DataFrame(columns=student_columns)

        # Write to Excel (only 1 sheet)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_students.to_excel(writer, index=False, sheet_name="Students")

        output.seek(0)

        return send_file(output,
                        as_attachment=True,
                        download_name="sample_students.xlsx",
                        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    @app.route('/upload_students', methods=['POST'])
    def upload_students():
        file = request.files.get('file')
        if not file:
            flash("No file uploaded", "error")
            return redirect(url_for('Add_bulk_student'))

        try:
            # Read Excel file
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip().str.lower()  # normalize column names
        except Exception as e:
            flash(f"Error reading Excel file: {str(e)}", "error")
            return redirect(url_for('Add_bulk_student'))

        required_columns = ["name","enrollment number", "email", "phone", "address", "date_of_birth","date_of_addmission",
                            "gender", "father_name", "mother_name", "nationality", "religion", "category",
                            "acadamic_year", "department", "standard", "division"]

        # Check for missing columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            flash(f"Missing columns: {', '.join(missing_cols)}", "error")
            return redirect(url_for('Add_bulk_student'))

        inserted = 0
        errors = []
        new_students_list = []

        for index, row in df.iterrows():
            try:
                # Validate Academic Year
                acad_year = AcadamicYear.query.filter_by(year_name=row["acadamic_year"]).first()
                if not acad_year:
                    errors.append(f"Row {index+2}: Invalid Academic Year '{row['acadamic_year']}'")
                    continue

                # Validate Department
                dept = Departments.query.filter_by(department_name=row["department"]).first()
                if not dept:
                    errors.append(f"Row {index+2}: Invalid Department '{row['department']}'")
                    continue

                # Validate Standard
                std = Standards.query.filter_by(name=row["standard"]).first()
                if not std:
                    errors.append(f"Row {index+2}: Invalid Standard '{row['standard']}'")
                    continue

                # Validate Division
                div = Division.query.filter_by(name=row["division"]).first()
                if not div:
                    errors.append(f"Row {index+2}: Invalid Division '{row['division']}'")
                    continue

                # Check duplicate email
                if Students.query.filter_by(email=row["email"]).first():
                    errors.append(f"Row {index+2}: Duplicate Email '{row['email']}'")
                    continue

                # Create Student object
                new_student = Students(
                    name=row["name"],
                    enrollment_number=row["enrollment number"],
                    email=row["email"],
                    phone=row["phone"],
                    address=row["address"],
                    date_of_birth=row["date_of_birth"],
                    date_of_addmission=row["date_of_addmission"],
                    gender=row["gender"],
                    father_name=row["father_name"],
                    mother_name=row["mother_name"],
                    nationality=row["nationality"],
                    religion=row["religion"],
                    category=row["category"],
                    acadamic_year_id=acad_year.id,
                    department_id=dept.id,
                    standard_id=std.id,
                    division_id=div.id
                )
                new_students_list.append(new_student)
                inserted += 1

            except Exception as e:
                errors.append(f"Row {index+2}: {str(e)}")

        # Bulk insert
        if new_students_list:
            db.session.bulk_save_objects(new_students_list)
            db.session.commit()

        # Flash messages
        if inserted:
            flash(f"{inserted} students added successfully.", "addstudentsuccess")
        if errors:
            flash("Errors:\n" + "\n".join(errors), "addstudenterror")

        return redirect(url_for('Add_bulk_student'))
    @app.route('/student_dashboard', methods=['GET', 'POST'])
    def student_dashboard():
        years = AcadamicYear.query.all()
        departments = Departments.query.all()
        standards = Standards.query.all()
        divisions = Division.query.all()
        
        students = []  # default empty
        selected_filters = {
            'acadamic_year': None,
            'department_id': None,
            'standard_id': None,
            'division_id': None
        }

        if request.method == 'POST':
            selected_filters['acadamic_year'] = request.form.get('acadamic_year')
            selected_filters['department_id'] = request.form.get('department_id')
            selected_filters['standard_id'] = request.form.get('standard_id')
            selected_filters['division_id'] = request.form.get('division_id')

            # Only fetch students if all filters are selected
            if all(selected_filters.values()):
                students = Students.query.filter_by(
                    acadamic_year_id=selected_filters['acadamic_year'],
                    department_id=selected_filters['department_id'],
                    standard_id=selected_filters['standard_id'],
                    division_id=selected_filters['division_id']
                ).all()
                if not students:
                    flash("No students found for the selected criteria.","nostudent")

        return render_template(
            'student_dashboard.html',
            years=years,
            departments=departments,
            standards=standards,
            divisions=divisions,
            students=students,
            selected_filters=selected_filters
        )
    @app.route('/delete_student/<int:student_id>', methods=['POST'])
    def delete_student(student_id):
        student = Students.query.get_or_404(student_id)
        try:
            db.session.delete(student)
            db.session.commit()
            flash("Student deleted successfully!", "deletesuccess")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting student: {str(e)}", "deleteerror")
        return redirect(url_for('student_dashboard',acadamic_year=request.form.get('acadamic_year'),
                            department_id=request.form.get('department_id'),
                            standard_id=request.form.get('standard_id'),
                            division_id=request.form.get('division_id')))
    @app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
    def edit_student(student_id):
        student = Students.query.get_or_404(student_id)
        years = AcadamicYear.query.all()
        departments = Departments.query.all()
        standards = Standards.query.all()
        divisions = Division.query.all()

        if request.method == 'POST':
            student.name = request.form['name']
            student.enrollment_number = request.form['enrollment_number']
            student.email = request.form['email']
            student.phone = request.form['phone']
            student.address = request.form['address']
            student.date_of_birth = request.form['dob']
            student.date_of_addmission = request.form['doa']
            student.gender = request.form['gender']
            student.father_name = request.form['father_name']
            student.mother_name = request.form['mother_name']
            student.nationality = request.form['nationality']
            student.religion = request.form['religion']
            student.category = request.form['category']
            student.acadamic_year_id = request.form['acadamic_year']
            student.department_id = request.form['department_id']
            student.standard_id = request.form['standard_id']
            student.division_id = request.form['division_id']
            db.session.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for('student_dashboard'))
        

        return render_template('editstudent.html', student=student, years=years, departments=departments, standards=standards, divisions=divisions)
    @app.route('/bulk_delete_students', methods=['POST'])
    def bulk_delete_students():
        student_ids = request.form.get('student_ids')
        if student_ids:
            ids_list = student_ids.split(',')
            Students.query.filter(Students.id.in_(ids_list)).delete(synchronize_session=False)
            db.session.commit()
            flash(f'{len(ids_list)} students deleted successfully!', 'success')
        else:
            flash('No students selected.', 'error')
        return redirect(url_for('student_dashboard'))
    @app.route('/export_students', methods=['POST'])
    def export_students():
        from io import StringIO
        import csv

        # 1️⃣ Get selected student IDs (agar checkbox se aaye ho)
        student_ids = request.form.get('student_ids', '')
        student_ids = [int(sid) for sid in student_ids.split(',') if sid.strip().isdigit()]

        # 2️⃣ Get filters
        acadamic_year = request.form.get('acadamic_year')
        department_id = request.form.get('department_id')
        standard_id = request.form.get('standard_id')
        division_id = request.form.get('division_id')

        # 3️⃣ Query base
        query = Students.query

        # agar selected students diye hain → wahi export karo
        if student_ids:
            query = query.filter(Students.id.in_(student_ids))

        # agar selected nahi, lekin filter diya gaya hai → filter apply karo
        elif any([acadamic_year, department_id, standard_id, division_id]):
            if acadamic_year:
                query = query.filter_by(acadamic_year_id=acadamic_year)
            if department_id:
                query = query.filter_by(department_id=department_id)
            if standard_id:
                query = query.filter_by(standard_id=standard_id)
            if division_id:
                query = query.filter_by(division_id=division_id)

        # agar na select na filter → sabhi students
        else:
            query = Students.query

        students = query.all()

        # agar koi student hi nahi mila
        if not students:
            flash("No students found for export.", "error")
            return redirect(url_for('students_page'))

        # 4️⃣ CSV generate karo
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            'Academic Year', 'Department', 'Standard', 'Division',
            'Name','Enrollment number','Email', 'Phone', 'Address', 'Date of Birth',
            'Gender', 'Father Name', 'Mother Name', 'Nationality', 'Religion', 'Category',
            'Date of admission'
        ])

        for s in students:
            writer.writerow([
                s.acadamic_year.year_name if s.acadamic_year else '',
                s.department.department_name if s.department else '',
                s.standard.name if s.standard else '',
                s.division.name if s.division else '',
                s.name,
                s.enrollment_number,
                s.email,
                s.phone,
                s.address,
                s.date_of_birth.strftime('%Y-%m-%d') if s.date_of_birth else '',
                s.gender if s.gender else '',
                s.father_name if s.father_name else '',
                s.mother_name if s.mother_name else '',
                s.nationality if s.nationality else '',
                s.religion if s.religion else '',
                s.category if s.category else '',
                s.date_of_addmission.strftime('%Y-%m-%d') if s.date_of_addmission else '',
               
            ])

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='filtered_students.csv'
        )   
    @app.route('/faculty_departments', methods=['GET', 'POST'])
    def faculty_departments():
        if request.method == 'POST':
            faculty_dept_name = request.form.get('faculty_department')
            if faculty_dept_name:
                existing = Faculty_Department.query.filter_by(name=faculty_dept_name).first()
                if existing:
                    flash("Faculty Department already exists!", "faculty_dept_error")
                else:
                    new_faculty_dept = Faculty_Department(name=faculty_dept_name)
                    try:
                        db.session.add(new_faculty_dept)
                        db.session.commit()
                        flash("Faculty Department added successfully!", "faculty_dept_success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding Faculty Department: {str(e)}", "faculty_dept_error")
            return redirect(url_for('faculty_departments'))
    
        departments_list = Faculty_Department.query.all()
        return render_template('faculty_department.html', departments=departments_list)


    @app.route('/faculty_departments/edit/<int:id>', methods=['POST'])
    def edit_faculty_department(id):
        new_dept = request.form.get('faculty_department')
        dept = Faculty_Department.query.get_or_404(id)
        dept.name = new_dept
        db.session.commit()
        flash("Faculty Department updated successfully!", "faculty_dept_success")
        return redirect(url_for('faculty_departments'))


    @app.route('/faculty_departments/delete/<int:id>', methods=['POST', 'GET'])
    def delete_faculty_department(id):
        dept = Faculty_Department.query.get_or_404(id)
        if hasattr(dept, 'faculties') and dept.faculties:
            flash("Cannot delete Faculty Department because faculties exist for this department.", "faculty_dept_error")
            return redirect(url_for('faculty_departments'))
        db.session.delete(dept)
        db.session.commit()
        flash("Faculty Department deleted successfully!", "faculty_dept_success")
        return redirect(url_for('faculty_departments'))
    @app.route('/Add_faculty', methods=['GET', 'POST'])
    def Add_faculty():
        if request.method == 'POST':
            try:
                name = request.form.get('name')
                fmid = request.form.get('fmid')
                email = request.form.get('email')
                phone = request.form.get('phone')
                gender = request.form.get('gender')
                address = request.form.get('address')
                city = request.form.get('city')
                state = request.form.get('state')
                pincode = request.form.get('pincode')
                date_of_birth = request.form.get('dob')
                joining_date = request.form.get('doj')
                qualification = request.form.get('qualification')
                experience = request.form.get('experience')
                faculty_department_id= request.form.get('department_id')

                # ✅ Check department first
                if not faculty_department_id:
                    flash("Error: Department dropdown must be selected!", "Facultydropdownerror")
                    return redirect(url_for('Add_faculty'))

                # ✅ Check duplicate email or phone
                existing_faculty = Faculty.query.filter(
                    (Faculty.email == email) | (Faculty.phone == phone)
                ).first()
                if existing_faculty:
                    flash("Error: Faculty with this email or phone already exists!", "FacultyEmailerror")
                    return redirect(url_for('Add_faculty'))

                # ✅ Add new faculty
                new_faculty = Faculty(
                    name=name,
                    fmid=fmid,
                    email=email,
                    phone=phone,
                    gender=gender,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    date_of_birth=date_of_birth,
                    joining_date=joining_date,
                    qualification=qualification,
                    experience=experience,
                    faculty_department_id=faculty_department_id
                )

                db.session.add(new_faculty)
                db.session.commit()
                flash("Faculty added successfully!", "Facultyaddsuccess")
                return redirect(url_for('Add_faculty'))

            except Exception as e:
                db.session.rollback()
                flash(f"Error adding faculty: {str(e)}", "Facultyadderror")
                return redirect(url_for('Add_faculty'))

        # ✅ Send dropdown data to template
        departments = Faculty_Department.query.all()
        return render_template('addfaculty.html', departments=departments)
    @app.route('/Add_bulk_faculty')
    def Add_bulk_faculty():
        return render_template('addbulkfaculty.html')
    @app.route('/download_sample_excel_faculty')
    def download_sample_excel_faculty():
        # Create a sample Excel file
        faculty_columns = ["Full name", "Faculty ID", "Email", "Phone number", "Gender", "Address", "City", "State", "pincode", 
                           "Date_of_date", "Date_of_joining", "qualification", "Experience", "Department"]
        df_faculty = pd.DataFrame(columns=faculty_columns)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_faculty.to_excel(writer, index=False, sheet_name="Faculty")
        output.seek(0)
        return send_file(output,
                         as_attachment=True,
                         download_name="sample_faculty.xlsx",
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    @app.route('/upload_faculty', methods=['POST'])
    def upload_faculty():
        file = request.files.get('file')
        if not file:
            flash("No file uploaded", "addfacultyerror")
            return redirect(url_for('Add_bulk_faculty'))

        try:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip().str.lower()
        except Exception as e:
            flash(f"Error reading Excel file: {str(e)}", "addfacultyerror")
            return redirect(url_for('Add_bulk_faculty'))

        required_columns = ["full name", "faculty id", "email", "phone number", "gender", "address", "city", "state", "pincode", 
                            "date_of_date", "date_of_joining", "qualification", "experience", "department"]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            flash(f"Missing columns: {', '.join(missing_cols)}", "addfacultyerror")
            return redirect(url_for('Add_bulk_faculty'))
        inserted = 0
        errors = []
        new_faculty_list = []
        for index, row in df.iterrows():
            try:
                dept = Faculty_Department.query.filter_by(name=row["department"]).first()
                if not dept:
                    errors.append(f"Row {index+2}: Invalid Department '{row['department']}'")
                    continue
                if Faculty.query.filter_by(phone=row["phone number"]).first():
                    errors.append(f"Row {index+2}: Duplicate Phone Number '{row['phone number']}'")
                    continue
                if Faculty.query.filter_by(email=row["email"]).first():
                    errors.append(f"Row {index+2}: Duplicate Email '{row['email']}'")
                    continue
                if Faculty.query.filter_by(fmid=row["faculty id"]).first():
                    errors.append(f"Row {index+2}: Duplicate Faculty ID '{row['faculty id']}'")
                    continue
                new_faculty = Faculty(
                    name=row["full name"],
                    fmid=row["faculty id"],
                    email=row["email"],
                    phone=row["phone number"],
                    gender=row["gender"],
                    address=row["address"],
                    city=row["city"],
                    state=row["state"],
                    pincode=row["pincode"],
                    date_of_birth=row["date_of_date"],
                    joining_date=row["date_of_joining"],
                    qualification=row["qualification"],
                    experience=row["experience"],
                    faculty_department_id=dept.id
                )
                new_faculty_list.append(new_faculty)
                inserted += 1
            except Exception as e:
                errors.append(f"Row {index+2}: {str(e)}")
        if new_faculty_list:
            db.session.bulk_save_objects(new_faculty_list)
            db.session.commit()
        if inserted:
            flash(f"{inserted} faculty members added successfully.", "addfacultysuccess")
        if errors:
            flash("Errors:\n" + "\n".join(errors), "addfacultyerror")
        return redirect(url_for('Add_bulk_faculty'))
    @app.route('/faculty_dashboard', methods=['GET', 'POST'])
    def faculty_dashboard():
        departments = Faculty_Department.query.all()
        faculty_list = []   # same name as template

        selected_filters = {
            'faculty_department_id': None
        }

        if request.method == 'POST':
            selected_filters['faculty_department_id'] = request.form.get('faculty_department_id')

            if selected_filters['faculty_department_id']:
                dept_id = int(selected_filters['faculty_department_id'])  # 🔥 FIX

                faculty_list = Faculty.query.filter_by(
                    faculty_department_id=dept_id
                ).all()

                if not faculty_list:
                    flash("No faculties found for the selected criteria.", "nofaculty")

        return render_template(
            'faculty_dashboard.html',
            departments=departments,
            faculty_list=faculty_list,
            selected_filters=selected_filters
        )
    @app.route('/delete_faculty/<int:faculty_id>', methods=['POST'])
    def delete_faculty(faculty_id):
        faculty = Faculty.query.get_or_404(faculty_id)
        try:
            db.session.delete(faculty)
            db.session.commit()
            flash("Faculty deleted successfully!", "Facultydeletesuccess")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting faculty: {str(e)}", "Facultydeleteerror")
        return redirect(url_for('faculty_dashboard',faculty_department_id=request.form.get('faculty_department_id')))
    @app.route('/export_faculty', methods=['POST'])
    def export_faculty():
        from io import StringIO
        import io
        import csv

        # 1️⃣ Get selected faculty IDs (agar checkbox se aaye ho)
        faculty_ids = request.form.get('faculty_ids', '')
        faculty_ids = [int(fid) for fid in faculty_ids.split(',') if fid.strip().isdigit()]
        
        # 2️⃣ Get filters
        faculty_department_id = request.form.get('faculty_department_id', type=int)
        # 3️⃣ Query base
        query = Faculty.query
        # agar selected faculties diye hain → wahi export karo
        if faculty_ids:
            query = query.filter(Faculty.id.in_(faculty_ids))
        # agar selected nahi, lekin filter diya gaya hai → filter apply karo
        elif faculty_department_id:
            query = query.filter_by(faculty_department_id=faculty_department_id)
        # agar na select na filter → sabhi faculties
        else:
            query = Faculty.query
        faculties = query.all()
        # agar koi faculty hi nahi mila
        if not faculties:
            flash("No faculties found for export.", "error")
            return redirect(url_for('faculty_dashboard'))
        # 4️⃣ CSV generate karo
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'faculty_department','Faculty ID', 'Name', 'Email', 'Phone', 'Gender', 'Address', 'City', 'State', 'Pincode',
            'date_of_birth','joining_date','qualification','experience'])
        for f in faculties:
            writer.writerow([
                f.Faculty_Department.name if f.Faculty_Department else '',
                f.fmid,
                f.name,
                f.email,
                f.phone,
                f.gender,
                f.address,
                f.city,
                f.state,
                f.pincode,
                f.date_of_birth.strftime('%Y-%m-%d') if f.date_of_birth else '',
                f.joining_date.strftime('%Y-%m-%d') if f.joining_date else '',
                f.qualification if f.qualification else '',
                f.experience if f.experience else ''
            ])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='filtered_faculty.csv'
        )
    @app.route('/bulk_delete_faculty', methods=['POST'])
    def bulk_delete_faculty():
        faculty_ids = request.form.get('faculty_ids')
        if faculty_ids:
            ids_list = faculty_ids.split(',')
            Faculty.query.filter(Faculty.id.in_(ids_list)).delete(synchronize_session=False)
            db.session.commit()
            flash(f'{len(ids_list)} faculty members deleted successfully!', 'facultysuccess')
        else:
            flash('No faculty members selected.', 'facultyerror')
        return redirect(url_for('faculty_dashboard'))
    @app.route('/edit_faculty/<int:faculty_id>', methods=['GET', 'POST'])
    def edit_faculty(faculty_id):
        faculty = Faculty.query.get_or_404(faculty_id)
        departments = Faculty_Department.query.all()

        if request.method == 'POST':
            faculty.name = request.form['name']
            faculty.fmid = request.form['fmid']
            faculty.email = request.form['email']
            faculty.phone = request.form['phone']
            faculty.gender = request.form['gender']
            faculty.address = request.form['address']
            faculty.city = request.form['city']
            faculty.state = request.form['state']
            faculty.pincode = request.form['pincode']
            faculty.date_of_birth = request.form['dob']
            faculty.joining_date = request.form['doj']
            faculty.qualification = request.form['qualification']
            faculty.experience = request.form['experience']
            faculty.faculty_department_id = request.form['department']
            db.session.commit()
            flash("Faculty updated successfully!", "editfacultysuccess")
            return redirect(url_for('faculty_dashboard'))
        return render_template('editfaculty.html', faculty=faculty, departments=departments)
            
    @app.route('/medium' , methods=['GET','POST'])
    def medium():
        if request.method=="POST":
            medium_name=request.form.get('medium_name')
            if medium_name:
                existing=Medium.query.filter_by(name=medium_name).first()
                if existing:
                    flash("Medium is already exist","mediumerror")
                else:
                    new_medium=Medium(name=medium_name)
                    try:
                        db.session.add(new_medium)
                        db.session.commit()
                        flash("Medium added sucessfully" , "sucessmedium")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error in adding medium:{str(e)}","errormedium")
            return redirect(url_for('medium'))
        all_medium=Medium.query.all()
        return render_template('medium.html',Medium=all_medium)     
    @app.route('/medium/edit/<int:id>',methods=['GET','POST'])
    def Edit_medium(id):
        medium=Medium.query.get_or_404(id)
        if request.method=='POST':
            new_medium=request.form.get('medium_name')
            medium.name=new_medium
            db.session.commit()
            flash("Medium updated successfully!","successmedium")
            return redirect(url_for('medium'))
    @app.route('/medium/delete/<int:id>',methods=['POST','GET'])
    def Delete_medium(id):
        medium=Medium.query.get_or_404(id)
        if medium.students:
            flash("Cannot delete Medium Because students already exist for this Medium.","deletemediumerror")
            return redirect(url_for('medium'))
        db.session.delete(medium)
        db.session.commit()
        flash("Medium deleted successfully!","successmedium")
        return redirect(url_for('medium'))
                
    return app
    


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
