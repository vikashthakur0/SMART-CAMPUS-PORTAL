# numbers for the system report

import database
from models import ADMIN, FACULTY, STUDENT


def generate_summary():
    users = database.get_all_users()
    courses = database.get_all_courses()

    active_users = [u for u in users if u.is_active]
    active_courses = [c for c in courses if c.is_active]

    enrollments = 0
    for c in active_courses:
        enrollments += len(c.student_ids)

    roles = {STUDENT: 0, FACULTY: 0, ADMIN: 0}
    for u in active_users:
        roles[u.role] += 1

    if len(active_courses) > 0:
        average = round(enrollments / len(active_courses), 1)
    else:
        average = 0

    return {
        "total_active_users": len(active_users),
        "role_distribution": roles,
        "active_courses": len(active_courses),
        "total_enrollments": enrollments,
        "avg_enrollment_per_course": average,
    }


def format_report(summary):
    dist = summary["role_distribution"]
    lines = [
        "=" * 40,
        "        SYSTEM SUMMARY REPORT",
        "=" * 40,
        "Total active users      : " + str(summary["total_active_users"]),
        "  Students              : " + str(dist[STUDENT]),
        "  Faculty               : " + str(dist[FACULTY]),
        "  Admins                : " + str(dist[ADMIN]),
        "Active courses          : " + str(summary["active_courses"]),
        "Total enrollments       : " + str(summary["total_enrollments"]),
        "Avg. students per course: " + str(summary["avg_enrollment_per_course"]),
        "=" * 40,
    ]
    return "\n".join(lines)
