# creating courses and enrolling in them

import logging

import database
from models import FACULTY, STUDENT, Course
from utils import ValidationError

log = logging.getLogger(__name__)


def create_course(faculty, code, title, capacity=60):
    if faculty.role != FACULTY:
        raise ValidationError("Only faculty can create courses.")
    code = (code or "").strip().upper()
    title = (title or "").strip()
    if code == "" or title == "":
        raise ValidationError("Course code and title are both required.")
    try:
        capacity = int(capacity)
    except ValueError:
        raise ValidationError("Capacity must be a whole number.")
    if capacity < 1 or capacity > 500:
        raise ValidationError("Capacity must be between 1 and 500.")
    for c in database.get_all_courses():
        if c.code == code:
            raise ValidationError("A course with code " + code + " already exists.")

    course = Course(code, title, faculty.user_id, capacity)
    database.add_course(course)
    log.info("Course %s created by %s", code, faculty.email)
    return course


def list_courses():
    result = []
    for c in database.get_all_courses():
        if c.is_active:
            result.append(c)
    return result


def enroll(student, course_id):
    if student.role != STUDENT:
        raise ValidationError("Only students can enroll in courses.")
    course = database.find_course((course_id or "").strip().upper())
    if course is None or not course.is_active:
        raise ValidationError("No active course found with that ID.")
    if student.user_id in course.student_ids:
        raise ValidationError("You are already enrolled in this course.")
    if course.is_full():
        raise ValidationError("Sorry, this course is full.")

    course.student_ids.append(student.user_id)
    database.update_course(course)
    log.info("%s enrolled in %s", student.email, course.code)
    return course


def courses_for_student(student):
    result = []
    for c in list_courses():
        if student.user_id in c.student_ids:
            result.append(c)
    return result


def courses_for_faculty(faculty):
    result = []
    for c in list_courses():
        if c.faculty_id == faculty.user_id:
            result.append(c)
    return result
