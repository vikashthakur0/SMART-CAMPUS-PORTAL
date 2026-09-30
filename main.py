# command line part of the Smart Campus Portal. Run with: python main.py

import logging

import auth_service
import course_service
import report_service
from utils import ValidationError

logging.basicConfig(
    filename="campus.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def print_courses(courses):
    if len(courses) == 0:
        print("  (no courses to show)")
        return
    for c in courses:
        print("  " + c.course_id + " | " + c.code + " | " + c.title +
              " | seats left: " + str(c.seats_left) + "/" + str(c.capacity))


def register_screen():
    print("\n--- Register ---")
    name = input("Full name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ")      # password is visible now
    role = input("Role (student/faculty): ").strip()
    try:
        user = auth_service.register(name, email, password, role)
        print("Welcome, " + user.name + "! Your account has been created. You can log in now.")
    except ValidationError as err:
        print("Could not register: " + str(err))


def login_screen():
    print("\n--- Login ---")
    email = input("Email: ").strip()
    password = input("Password: ")      # password is visible now
    try:
        user = auth_service.login(email, password)
    except ValidationError as err:
        print("Login failed: " + str(err))
        return
    dashboard(user)


def dashboard(user):
    while True:
        options = user.dashboard_options() + ["Log out"]
        print("\n=== " + user.role.title() + " dashboard: " + user.name + " ===")
        for i in range(len(options)):
            print(str(i + 1) + ". " + options[i])
        choice = input("Choose an option: ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
            print("Please enter one of the numbers shown.")
            continue
        action = options[int(choice) - 1]
        if action == "Log out":
            print("Logged out. See you soon!")
            return
        handle_action(user, action)


def handle_action(user, action):
    try:
        if action == "Create a course":
            code = input("Course code (e.g. CSE1001): ").strip()
            title = input("Course title: ").strip()
            capacity = input("Capacity [60]: ").strip() or "60"
            course = course_service.create_course(user, code, title, capacity)
            print("Course created. Share this ID with students: " + course.course_id)
        elif action == "Browse courses":
            print_courses(course_service.list_courses())
        elif action == "Enroll in a course":
            print_courses(course_service.list_courses())
            course = course_service.enroll(user, input("Enter the course ID: "))
            print("You are now enrolled in " + course.code + " - " + course.title + ".")
        elif action == "My courses":
            if user.role == "student":
                print_courses(course_service.courses_for_student(user))
            else:
                print_courses(course_service.courses_for_faculty(user))
        elif action == "View system report":
            print(report_service.format_report(report_service.generate_summary()))
        elif action == "View profile":
            print("\nName : " + user.name)
            print("Email: " + user.email)
            print("Role : " + user.role)
            print("ID   : " + user.user_id)
        elif action == "Update profile":
            auth_service.update_name(user, input("New name: "))
            print("Profile updated.")
        elif action == "Change password":
            old = input("Current password: ")
            new = input("New password: ")
            auth_service.change_password(user, old, new)
            print("Password changed.")
    except ValidationError as err:
        print("Oops: " + str(err))


def main():
    print("Welcome to the Smart Campus Portal")
    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            login_screen()
        elif choice == "2":
            register_screen()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
