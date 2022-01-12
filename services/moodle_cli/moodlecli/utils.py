import string
import random

CSV_INST_FNAME = 'instructor_firstname'
CSV_INST_LNAME = 'instructor_lastname'
CSV_INST_EMAIL = 'instructor_email'
CSV_INST_AUTH = 'instructor_auth_type'
CSV_COURSE_NAME = 'course_name'
CSV_COURSE_SHORTNAME = 'course_shortname'
CSV_COURSE_CATEGORY = 'course_category'
CSV_COURSE_ID = "course_id"
CSV_COURSE_ENROLMENT_URL = "course_enrolment_url"
CSV_COURSE_ENROLMENT_KEY = "course_enrolment_key"


def generate_password(length=12):
    """Create a password value"""
    # We incorporate at least 1 digit, 1 upper case, 1 lower case, and
    # 1 non-alphanumeric

    non_alphanum = ".,;:!?_-+/*@#&$"

    password = []
    password.append(random.choice(string.digits))
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(non_alphanum))

    all_characters = string.digits + string.ascii_uppercase + \
        string.ascii_lowercase + non_alphanum
    password += random.choices(
        all_characters,
        k=max(0, length - len(password))
    )

    random.shuffle(password)
    return ''.join(password)


def course_bulk_input_csv_fieldnames():
    """Return array of fieldnames used / expected in input CSV for course
    bulk setup"""
    return [
        CSV_INST_FNAME,
        CSV_INST_LNAME,
        CSV_INST_EMAIL,
        CSV_INST_AUTH,
        CSV_COURSE_NAME,
        CSV_COURSE_SHORTNAME,
        CSV_COURSE_CATEGORY
    ]


def course_bulk_output_csv_fieldnames():
    """Return array of fieldnames in output CSV for course bulk setup"""
    return course_bulk_input_csv_fieldnames() + [
        CSV_COURSE_ID,
        CSV_COURSE_ENROLMENT_URL,
        CSV_COURSE_ENROLMENT_KEY
    ]


def create_or_get_user(moodle_client, firstname, lastname, email, auth):
    """Create a user account if it doesn't exist and return user ID"""
    existing_user = moodle_client.get_user_by_email(
        email
    )
    if existing_user:
        user_id = existing_user['id']
    else:
        new_user = moodle_client.create_user(
            firstname,
            lastname,
            email,
            auth
        )
        user_id = new_user["id"]
    return user_id


def setup_duplicate_course(
    moodle_client, base_course_id, coursedata, instructor_role_id,
    student_role_id
):
    """Setup a new course using a base and data from bulk CSV"""
    # Retrieve or create teacher account
    instructor_user_id = create_or_get_user(
        moodle_client,
        coursedata[CSV_INST_FNAME],
        coursedata[CSV_INST_LNAME],
        coursedata[CSV_INST_EMAIL],
        coursedata[CSV_INST_AUTH]
    )

    # Create a duplicate course using the base course
    new_course = moodle_client.copy_course(
        base_course_id,
        coursedata[CSV_COURSE_NAME],
        coursedata[CSV_COURSE_SHORTNAME],
        coursedata[CSV_COURSE_CATEGORY]
    )
    new_course_id = new_course["id"]

    # Enrol teacher user as a course instructor
    moodle_client.enrol_user(
        new_course_id,
        instructor_user_id,
        instructor_role_id
    )

    # Get enrolment ID for course and student role
    enrolments = moodle_client.get_self_enrolment_methods(
        new_course_id,
        student_role_id
    )
    if len(enrolments) != 1:
        raise Exception(
            "Unexpected number of student self enrolment methods found "
            f"for course {new_course_id}"
        )
    student_enrolment_id = enrolments[0]["id"]

    # Enable enrolment and set enrolment key
    moodle_client.enable_self_enrolment_method(student_enrolment_id)
    enrolment_key = generate_password()
    moodle_client.set_self_enrolment_method_key(
        student_enrolment_id,
        enrolment_key
    )

    # Return updated course dict adding course ID and enrolment URL / key
    coursedata[CSV_COURSE_ID] = new_course_id
    coursedata[CSV_COURSE_ENROLMENT_URL] = \
        moodle_client.get_course_enrolment_url(new_course_id)
    coursedata[CSV_COURSE_ENROLMENT_KEY] = enrolment_key

    return coursedata
