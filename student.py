# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# from db import db
# import pymysql
# from flask_wtf.csrf import CSRFProtect
# from werkzeug.security import check_password_hash
# from model import student
# from flask_mail import Mail, Message

# csrf = CSRFProtect()
   
#     @app.route('',methods=['GET','POST'])
#     def add_student():
#         if request.method=="POST":
#             name=request.form['name']
#             email=request.form['email']
#             phone=request.form['phone']
#             address=request.form['address']
#             date_of_birth=request.form['date_of_birth']
#             academic_year_id=request.form['academic_year_id']
            
#             new_student=students(name=name,email=email,phone=phone,address=address,date_of_birth=date_of_birth,academic_year_id=academic_year_ID)
#             db.session.add(new_student)
#             db.session.commit()
#             flash("Student add sucessfully","Student sucess")
#         return render_template("add_student_html.html")
            
            