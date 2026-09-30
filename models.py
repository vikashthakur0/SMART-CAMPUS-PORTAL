# classes for users and courses

from utils import generate_id

STUDENT = "student"
FACULTY = "faculty"
ADMIN = "admin"


class User:
    role = None

    def __init__(self, name, email, password_hash, salt, user_id=None, is_active=True):
        self.user_id = user_id or generate_id("USR")
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.salt = salt
        self.is_active = is_active

    def set_credentials(self, password_hash, salt):
        self.password_hash = password_hash
        self.salt = salt

    def dashboard_options(self):
        return ["View profile", "Update profile", "Change password"]

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "role": self.role,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"], data["password_hash"], data["salt"],
                   data["user_id"], data.get("is_active", True))


class Student(User):
    role = STUDENT

    def dashboard_options(self):
        return ["Browse courses", "Enroll in a course", "My courses"] + super().dashboard_options()


class Faculty(User):
    role = FACULTY

    def dashboard_options(self):
        return ["Create a course", "My courses", "View system report"] + super().dashboard_options()


class Admin(User):
    role = ADMIN

    def dashboard_options(self):
        return ["View system report", "Browse courses"] + super().dashboard_options()


ROLE_CLASSES = {STUDENT: Student, FACULTY: Faculty, ADMIN: Admin}


def user_from_dict(data):
    return ROLE_CLASSES[data["role"]].from_dict(data)


class Course:
    def __init__(self, code, title, faculty_id, capacity=60, course_id=None,
                 student_ids=None, is_active=True):
        self.course_id = course_id or generate_id("CRS")
        self.code = code
        self.title = title
        self.faculty_id = faculty_id
        self.capacity = capacity
        self.student_ids = list(student_ids or [])
        self.is_active = is_active

    @property
    def seats_left(self):
        return self.capacity - len(self.student_ids)

    def is_full(self):
        return self.seats_left <= 0

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "code": self.code,
            "title": self.title,
            "faculty_id": self.faculty_id,
            "capacity": self.capacity,
            "student_ids": self.student_ids,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["code"], data["title"], data["faculty_id"], data["capacity"],
                   data["course_id"], data["student_ids"], data["is_active"])
