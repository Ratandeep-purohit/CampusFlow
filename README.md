# 🎓 CampusFlow - Advanced Campus ERP System

[![Flask](https://img.shields.io/badge/Flask-v3.0+-blue?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **CampusFlow** is a modern, enterprise-grade Campus Management System (ERP) designed to streamline academic operations, centralize student/faculty data, and automate administrative workflows. Built with a focus on scalability and user experience.

---

## 🌟 Key Highlights (The "WOW" Factor)

- 🔐 **Role-Based Access Control (RBAC):** Secure authentication with distinct permissions for Admins, Faculty, and Students.
- 📂 **Bulk Data Management:** Seamlessly import hundreds of student records via Excel and export filtered data to CSV/Excel.
- 📊 **Dynamic Dashboards:** Real-time data visualization and advanced filtering for student and faculty management.
- ✉️ **Integrated Communication:** Automated feedback and notification system using SMTP/Flask-Mail.
- 🛠️ **Modular Architecture:** Highly scalable backend structure using Flask's Application Factory pattern.

---

## 🚀 Core Modules & Features

### 👨‍🎓 Student Management
- **Individual Enrollment:** Comprehensive forms capturing personal, academic, and category-wise details.
- **Bulk Import:** Robust Excel parser with error validation and duplicate checking using **Pandas**.
- **Interactive Dashboard:** Filter students by Academic Year, Department, Standard, and Division with real-time updates.
- **Data Portability:** Export data with one click for administrative reporting.

### 👩‍🏫 Faculty Management
- **Expertise Tracking:** Manage faculty records including qualifications, experience, and department-specific roles.
- **Dynamic Departments:** Flexible management of faculty-specific departments.

### 🏛️ Academic Configuration
- **Hierarchical Setup:** Define Academic Years, Departments, Standards (Grades), Divisions, and Mediums.
- **Contextual CRUD:** Easy management of all campus entities with integrated data validation.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :-- | :-- |
| **Backend** | Python, Flask, Flask-SQLAlchemy (ORM) |
| **Frontend** | HTML5, CSS3 (Modern UI), JavaScript (ES6+) |
| **Database** | MySQL / MariaDB |
| **Data Processing** | Pandas, Openpyxl, XlsxWriter |
| **Security** | Flask-WTF (CSRF), Werkzeug (Hashing) |
| **Mail/Logs** | Flask-Mail, SMTP Protocol |

---

## 📂 Project Structure

```bash
CampusFlow/
├── app.py             # Application Factory & Routes
├── model.py           # Database Schema (SQLAlchemy Models)
├── config.py          # Environment & App Configuration
├── db.py              # Database Initialization
├── static/            # CSS, JS, and Images
├── Templates/         # HTML Jinja2 Templates
├── migrations/        # Database Migration Scripts
└── Requirements.txt   # Project Dependencies
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ratandeep-purohit/CampusFlow.git
   cd CampusFlow
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r Requirements.txt
   ```

4. **Configure Environment**
   - Update `config.py` with your MySQL credentials.
   - Configure `MAIL_USERNAME` and `MAIL_PASSWORD` in `app.py` for feedback system.

5. **Run the Application**
   ```bash
   python app.py
   ```
   Access at: `http://127.0.0.1:5000`

---

## 📸 Preview

*(Add your high-quality screenshots here to double the impact!)*

---

## 🤝 Contact & Developer

**Ratandeep Purohit**  
*Full Stack Developer | ERP Solutions Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://linkedin.com/in/ratandeep-purohit)
[![Portfolio](https://img.shields.io/badge/View-Portfolio-red?style=flat&logo=web)](https://yourportfolio.com)
[![Email](https://img.shields.io/badge/Email-Contact-yellow?style=flat&logo=gmail)](mailto:rajatpurohit@gmail.com)

---
*Developed with Passion to simplify Education Management.*
