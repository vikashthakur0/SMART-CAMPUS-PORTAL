# Problem Statement

## The problem
Many campus systems are one big program where logins, course lists and reports are all mixed together. Passwords are sometimes stored as plain text, and adding one small feature can break other parts. Students and faculty get clumsy tools, and the people maintaining the code are afraid to change it.

## What this project does about it
The **Smart Campus Portal & Access Management System** is a small command-line portal that keeps the parts separate and safer:

- People register and log in, and their passwords are saved only as salted SHA-256 hashes.
- Every account has a role (Student, Faculty or Admin), and the role decides which menu options appear.
- Faculty create courses, students enroll in them, and a report shows how the campus is doing.
- The code is split into separate files (interface, models, database, services), so each part can be changed without touching the others.

## Scope
**In scope**
- Registration, login and profile management (change name, change password)
- Role-based dashboards
- Course creation and self-enrollment with seat limits
- A summary report (active users, role split, active courses, enrollments)
- Local JSON storage, input validation and unit tests

**Out of scope (for now)**
- A graphical or web interface
- Email verification and password reset by email
- Strong password rules and hidden password typing
- Grades, attendance, timetables and payments
- Many users using the data file at the same time

## Target users
| User | What they do here |
|------|-------------------|
| Student | Registers, browses courses, enrolls, views their own courses |
| Faculty | Creates courses, sees their own courses, views the system report |
| Admin | Views the system report and the course list |

## High-level features
1. **User authentication and access control**: registration, salted SHA-256 password hashing, regex email validation, role assignment.
2. **Course management**: faculty create courses, students self-enroll, with checks for duplicate and full courses.
3. **Analytics and reporting**: total active users, role distribution, active course count and enrollment numbers.
