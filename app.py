from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db import db
import csv
import pymysql
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from model import Register, AcadamicYear, Departments, Standards , Roles , Division , Students
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
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password!", "danger")
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
                    flash("Academic year already exists!", "error")
                else:
                    new_year = AcadamicYear(year_name=year)
                    try:
                        db.session.add(new_year)
                        db.session.commit()
                        flash("Academic year added successfully!", "success")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding academic year: {str(e)}", "error")
                return redirect(url_for('acadamic_year'))
        years = AcadamicYear.query.all()
        return render_template("acadamic_year.html", years=years)

    @app.route('/acadamic_years/edit/<int:id>', methods=['GET', 'POST'])
    def edit_acadamic_year(id):
        new_year = request.form.get('year_name')
        ay = AcadamicYear.query.get_or_404(id)
        ay.year_name = new_year
        db.session.commit()
        flash("Academic year updated successfully!", "success")
        return redirect(url_for('acadamic_year'))

    @app.route('/acadamic_years/delete/<int:id>', methods=['POST','GET'])
    def delete_acadamic_year(id):
        ay = AcadamicYear.query.get_or_404(id)
        if ay.students:
            flash("Cannot delete academic year Because students exist for this year.", "deleteacademicyearerror")
            return redirect(url_for('acadamic_year'))
        db.session.delete(ay)
        db.session.commit()
        flash("Academic year deleted successfully!", "success")
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
                        flash("Division added suce","sucess")
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding Division: {str(e)}","error")
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
            flash("Division updated successfully!","success")
            return redirect(url_for('Division_page'))
    @app.route('/Division/delete/<int:id>',methods=['POST','GET'])
    def Delete_Division(id):
        division=Division.query.get_or_404(id)
        db.session.delete(division)
        db.session.commit()
        flash("Division deleted successfully!","success")
        return redirect(url_for('Division_page'))
    @app.route('/Add_student', methods=['GET', 'POST'])
    def Add_student():
        if request.method == 'POST':
            try:
                name=request.form.get('name')
                email=request.form.get('email')
                phone=request.form.get('phone')
                address=request.form.get('address')
                date_of_birth=request.form.get('dob')
                
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
                    email=email,
                    phone=phone,
                    address=address,
                    date_of_birth=date_of_birth,
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
        student_columns = ["name", "email", "phone", "address", "date_of_birth",
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

        required_columns = ["name", "email", "phone", "address", "date_of_birth",
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
                    email=row["email"],
                    phone=row["phone"],
                    address=row["address"],
                    date_of_birth=row["date_of_birth"],
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
            student.email = request.form['email']
            student.phone = request.form['phone']
            student.address = request.form['address']
            student.date_of_birth = request.form['dob']
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
            'Name', 'Email', 'Phone', 'Address', 'Date of Birth',
            'Academic Year', 'Department', 'Standard', 'Division'
        ])

        for s in students:
            writer.writerow([
                s.name,
                s.email,
                s.phone,
                s.address,
                s.date_of_birth.strftime('%Y-%m-%d') if s.date_of_birth else '',
                s.acadamic_year.year_name if s.acadamic_year else '',
                s.department.department_name if s.department else '',
                s.standard.name if s.standard else '',
                s.division.name if s.division else ''
            ])

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='filtered_students.csv'
        )   
    return app
    


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
