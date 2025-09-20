# Student Report Management System (Django CRUD App)

A simple Django project for managing students and their grades in a school setting.
This app demonstrates the **CRUD (Create, Read, Update, Delete)** operations using Django’s **Models, Views, Templates, and Forms**.

---

## Features

* Add, edit, delete students
* Record and view grades per student
* List all students with details
* User-friendly Django Admin panel
* SQLite database (default)

---

##  Requirements

* Python 3.10+ (via Anaconda or standalone install)
* Django 5.x
* (Optional)

  * `django-crispy-forms` → better form styling
  * `django-debug-toolbar` → debugging support

---

## Setup Instructions

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

### 5️⃣ Create a superuser (to access admin)

```bash
python manage.py createsuperuser
```

### 6️⃣ Start the development server

```bash
python manage.py runserver
```

Visit  [http://127.0.0.1:8000/students/](http://127.0.0.1:8000/students/)

---

##  Project Structure

```
school_project/
│
├── reports/              # Django app for students & grades
│   ├── models.py         # Student, Grade models
│   ├── views.py          # CRUD views
│   ├── urls.py           # App routes
│   └── templates/        # HTML templates
│
├── school_project/       # Project settings
│   └── settings.py
│
├── db.sqlite3            # Default database
├── manage.py             # Django CLI tool
└── requirements.txt
```

---

##  Screenshots

* **Student List** – shows all students
* **Student Detail** – view grades per student
* **Admin Panel** – manage records easily

*(Add screenshots later after running the app)*

---

##  Learning Outcomes

* Understand Django’s **MTV (Model-Template-View)** workflow
* Implement full CRUD functionality
* Use Django Admin for quick data management
* Organize templates and static files in a real project
