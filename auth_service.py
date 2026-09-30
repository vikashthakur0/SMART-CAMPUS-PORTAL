# register, login and profile stuff

import logging

import database
from models import ROLE_CLASSES, STUDENT, FACULTY
from utils import (ValidationError, generate_salt, hash_password, validate_email,
                   validate_name, validate_password, verify_password)

log = logging.getLogger(__name__)


def register(name, email, password, role):
    name = validate_name(name)
    email = validate_email(email)
    validate_password(password)
    role = (role or "").strip().lower()
    if role != STUDENT and role != FACULTY:
        raise ValidationError("Role must be 'student' or 'faculty'.")
    if database.find_user_by_email(email):
        raise ValidationError("An account with this email already exists.")

    salt = generate_salt()
    user = ROLE_CLASSES[role](name, email, hash_password(password, salt), salt)
    database.add_user(user)
    log.info("Registered new %s: %s", role, email)
    return user


def login(email, password):
    email = (email or "").strip().lower()
    user = database.find_user_by_email(email)
    if user is None or not verify_password(password or "", user.salt, user.password_hash):
        log.warning("Failed login for %s", email)
        raise ValidationError("Incorrect email or password.")
    if not user.is_active:
        raise ValidationError("This account has been deactivated.")
    log.info("Login OK: %s (%s)", email, user.role)
    return user


def update_name(user, new_name):
    user.name = validate_name(new_name)
    database.update_user(user)
    return user


def change_password(user, old_password, new_password):
    if not verify_password(old_password or "", user.salt, user.password_hash):
        raise ValidationError("Current password is incorrect.")
    validate_password(new_password)
    salt = generate_salt()
    user.set_credentials(hash_password(new_password, salt), salt)
    database.update_user(user)
    log.info("Password changed for %s", user.email)
    return user
