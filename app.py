from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db import db
import pymysql
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from model import Register, AcadamicYear, Departments, Standards   # 👈 Standards import karo
from flask_mail import Message, Mail
from flask_migrate import Migrate

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Mail Config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'Rajatpurohit183@gmail.com'
    app.config['MAIL_PASSWORD'] = '198320072011'
    
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
        flash("Logged out successfully.", "info")
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
    @app.route('/Roles',method=['GET','Post'])
    def roles_page():
        return render_template('Roles.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
