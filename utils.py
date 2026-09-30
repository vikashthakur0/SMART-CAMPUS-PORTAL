# helper functions used by the other files

import hashlib
import os
import re
import uuid


class ValidationError(Exception):
    # used when the user types something wrong
    pass


def generate_salt():
    return os.urandom(16).hex()


def hash_password(password, salt):
    # hash of salt + password
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(password, salt, expected_hash):
    return hash_password(password, salt) == expected_hash


def validate_email(email):
    email = (email or "").strip().lower()
    # simple check: something@something.something
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
        raise ValidationError("That is not a valid email (example: name@college.edu).")
    return email


def validate_password(password):
    # only checking that it is not empty
    if not password:
        raise ValidationError("Password cannot be empty.")
    return password


def validate_name(name):
    name = (name or "").strip()
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters.")
    return name


def generate_id(prefix):
    return prefix + "-" + uuid.uuid4().hex[:8].upper()
