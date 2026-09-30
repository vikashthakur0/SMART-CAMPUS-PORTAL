# Smart Campus Portal & Access Management System

A command-line campus portal made with Python. It has three types of users (Student, Faculty and Admin), and each one sees a different menu. Faculty can create courses, students can enroll in them, and a report shows the current numbers.

## Overview
The whole project runs in the terminal with plain Python and no external libraries. All data is saved in a local file called `database.json`, which is created automatically the first time you run the program.

## Features
- **Login and registration**: register as a student or faculty, log in, view your profile, change your name and change your password.
- **Password safety**: passwords are not saved as plain text. Only a random salt and the SHA-256 hash are stored.
- **Email check**: emails are checked with a regex and duplicate emails are not allowed.
- **Role-based menus**: each role only sees the options it is allowed to use.
- **Course management**: faculty create courses with a seat limit, students browse and enroll.
- **Reports**: shows active users, how many of each role, active courses and enrollments.
- **Error messages**: wrong input shows a clear message instead of crashing.

## Technologies used
- Python 3.8 or newer (only standard library: `hashlib`, `re`, `json`, `logging`, `uuid`, `os`)
- JSON file for storage
- Git for version control

## OOP concepts used
- **Inheritance**: `Student`, `Faculty` and `Admin` extend the base `User` class.
- **Polymorphism**: each role overrides `dashboard_options()` to show its own menu.
- **Encapsulation**: only `database.py` reads and writes `database.json`, and the other files ask it for data.

## Project structure
```
smart-campus-portal/
├── main.py             # menus and screens (command line)
├── models.py           # User, Student, Faculty, Admin and Course classes
├── database.py         # the only file that reads/writes database.json
├── auth_service.py     # register, login, profile and password logic
├── course_service.py   # course creation and enrollment logic
├── report_service.py   # report numbers and formatting
├── utils.py            # hashing, validation and ID helpers
├── tests/              # unit tests
├── statement.md        # problem statement
├── report.pdf          # project report
└── README.md
```

## How to install and run
1. Install Python 3.8 or newer.
2. Download or clone the project and open a terminal in its folder:
   ```
   git clone <your-repo-url>
   cd smart-campus-portal
   ```
3. Start the portal:
   ```
   python main.py
   ```

Nothing else needs to be installed.

**Demo admin account** (created on the first run):
`admin@campus.edu` / `Admin@123`

## Quick walkthrough
1. Choose **Register**, make a Faculty account, then log in and pick **Create a course**. Note the course ID that is printed.
2. Log out, register a Student account, log in and pick **Enroll in a course**. Type the course ID.
3. Log in as Faculty or Admin and pick **View system report** to see the numbers change.

## How to run the tests
From the project folder:
```
python -m unittest discover -s tests -t .
```
The tests use a temporary database, so your real `database.json` is not changed.

## Screenshots
_Add screenshots of the login menu, a dashboard and the report here._

## Notes about passwords and data
- Passwords are typed in visible form (not hidden) and only need to be non-empty. This keeps the project simple, but a real system should hide the password and ask for a stronger one.
- `database.json` and `campus.log` are listed in `.gitignore` so user data is not uploaded to GitHub.
- Change the demo admin password before using the portal for anything real.
