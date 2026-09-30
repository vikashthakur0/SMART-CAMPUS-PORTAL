# this file reads and writes database.json, nothing else touches it

import json
import os

from models import Admin, Course, user_from_dict
from utils import generate_salt, hash_password

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")

# demo admin account
DEFAULT_ADMIN_EMAIL = "admin@campus.edu"
DEFAULT_ADMIN_PASSWORD = "Admin@123"


def set_db_path(path):
    global DB_PATH
    DB_PATH = path


def make_new_db():
    # new database with just the admin in it
    salt = generate_salt()
    admin = Admin("Campus Admin", DEFAULT_ADMIN_EMAIL,
                  hash_password(DEFAULT_ADMIN_PASSWORD, salt), salt)
    db = {"users": [admin.to_dict()], "courses": []}
    save_db(db)
    return db


def load_db():
    if not os.path.exists(DB_PATH):
        return make_new_db()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
        if "users" not in db or "courses" not in db:
            return make_new_db()
        return db
    except json.JSONDecodeError:
        # file is broken so start again
        return make_new_db()


def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


# ---- users ----

def get_all_users():
    users = []
    for u in load_db()["users"]:
        users.append(user_from_dict(u))
    return users


def find_user_by_email(email):
    for u in load_db()["users"]:
        if u["email"] == email:
            return user_from_dict(u)
    return None


def add_user(user):
    db = load_db()
    db["users"].append(user.to_dict())
    save_db(db)


def update_user(user):
    db = load_db()
    for i in range(len(db["users"])):
        if db["users"][i]["user_id"] == user.user_id:
            db["users"][i] = user.to_dict()
            save_db(db)
            return
    raise KeyError("User not found")


# ---- courses ----

def get_all_courses():
    courses = []
    for c in load_db()["courses"]:
        courses.append(Course.from_dict(c))
    return courses


def find_course(course_id):
    for c in load_db()["courses"]:
        if c["course_id"] == course_id:
            return Course.from_dict(c)
    return None


def add_course(course):
    db = load_db()
    db["courses"].append(course.to_dict())
    save_db(db)


def update_course(course):
    db = load_db()
    for i in range(len(db["courses"])):
        if db["courses"][i]["course_id"] == course.course_id:
            db["courses"][i] = course.to_dict()
            save_db(db)
            return
    raise KeyError("Course not found")
