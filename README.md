# Student Report Management System (Django CRUD App + Authentication)

A Django project for managing students, courses, achievements, and support tickets in a school setting.
This app demonstrates **CRUD operations** as well as **Authentication & Role-Based Dashboards** using Django’s **Models, Views, Templates, and Forms**.

---

## ✨ Features

### 🔐 Authentication

* User registration & login with roles:

  * **Students** → view/enroll courses, achievements, support tickets.
  * **Lecturers** → manage their courses & view enrolled students.
  * **Admins** → full CRUD on users, courses, clubs, opportunities, tickets.
* Role-based dashboards (redirects based on user type).
* Admins can create new users (students, lecturers, admins) and manage them.
* Support ticket system with **status updates** (Open, In Progress, Closed).

### 📘 Student Features

* Enroll in available courses
* Submit and track support tickets
* View personal achievements

### 🎓 Lecturer Features

* View courses they teach
* See enrolled students

### 🛠️ Admin Features

* Create, edit, delete **users** (student, lecturer, admin)
* Manage **courses, clubs, opportunities, achievements, tickets**
* Update ticket statuses

---

## ⚙️ Requirements

* Python 3.10+ (via Anaconda or standalone install)
* Django 5.x

Optional:

* `django-crispy-forms` → better form styling
* `django-debug-toolbar` → debugging support

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Sibitenda/school_project.git
cd school_project
```

### 2️⃣ Create a virtual environment (using conda or venv)

```bash
conda create -n django_env python=3.11
conda activate django_env
```

or with venv:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a superuser (to access Django admin)

```bash
python manage.py createsuperuser
```

### 6️⃣ Start the development server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and log in.

---

## 📂 Project Structure

```
school_project/
│
├── reports/                  # Main Django app
│   ├── models.py             # User Profile, Student, Course, etc.
│   ├── views.py              # CRUD + authentication views
│   ├── forms.py              # User creation, student forms, ticket forms
│   ├── urls.py               # App routes
│   └── templates/reports/    # Role-based dashboards
│
├── school_project/           # Project settings
│   └── settings.py
│
├── db.sqlite3                # Default database
├── manage.py                 # Django CLI tool
└── requirements.txt
```

---

## 📸 Screenshots (to add later)

* **Student Dashboard** – enrolled courses, achievements, support tickets.
* **Lecturer Dashboard** – courses taught, students list.
* **Admin Dashboard** – manage users, courses, clubs, tickets.

---

## 🎯 Learning Outcomes

* Understand Django’s **MTV (Model-Template-View)** workflow
* Implement full **CRUD functionality**
* Add **authentication & role-based access control**
* Build interactive dashboards for different roles
* Manage records both via **custom UI** and Django Admin
