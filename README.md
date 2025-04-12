# Moni: Personal Finance Tracker - Django Project

A secure and user-friendly Django web application to help users track their income, expenses, and budgets. This project includes a full authentication system (login, registration, logout, session management) and a personalized dashboard for each user.

---

##  Features

-  User Registration & Login (with session management)
-  Secure password handling (Django's built-in auth system)
-  User Dashboard with:
  - Income and Expense Tracker
  - Category-based breakdown
  - Monthly summaries
  - Budget management
-  Transaction history
-  Export data to CSV
-  Filter transactions by date, category, and type
-  Clean, responsive UI with Bootstrap or Tailwind (customizable)

---

##  Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5 and CSS3
- **Database:** SQLite
- **Authentication:** Django's built-in auth system

---

##  User Authentication System

###  Registration
- Users can sign up via a `/register/` route.
- Form includes:
  - Username (unique)
  - Email
  - Password (encrypted)
- Backend uses Django's `UserCreationForm`.

###  Login
- Users can log in at `/login/`.
- Credentials validated using Django's `AuthenticationForm`.
- After login, users are redirected to their **personal dashboard**.

###  Logout
- Logout endpoint: `/logout/`
- Uses `django.contrib.auth.logout()` to terminate the session securely.

###  Session Handling
- Session cookies managed securely using Django's session middleware.
- CSRF protection enabled on all forms.
- User-specific data filtered using `request.user`.

---

##  Security Features

-  Passwords stored using Django's PBKDF2 hasher (configurable)
-  CSRF tokens for all POST forms
-  HTTPS recommended for deployment
-  Input validation and form error handling

---

##  Setup Instructions

```bash
# Clone the repository and Install Dependencies
git clone https://github.com/MarcKyle/moni-project.git
pip install -r requirements.txt
cd myproject

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```