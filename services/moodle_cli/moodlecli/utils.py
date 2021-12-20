import string
import random

COURSE_BULK_CSV_INST_FNAME = 'instructor_firstname'
COURSE_BULK_CSV_INST_LNAME = 'instructor_lastname'
COURSE_BULK_CSV_INST_EMAIL = 'instructor_email'
COURSE_BULK_CSV_INST_AUTH = 'instructor_auth_type'
COURSE_BULK_CSV_COURSE_NAME = 'course_name'
COURSE_BULK_CSV_COURSE_SHORTNAME = 'course_shortname'
COURSE_BULK_CSV_COURSE_CATEGORY = 'course_category'
COURSE_BULK_CSV_COURSE_ID = "course_id"
COURSE_BULK_CSV_COURSE_ENROLMENT_URL = "course_enrolment_url"
COURSE_BULK_CSV_COURSE_ENROLMENT_KEY = "course_enrolment_key"


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
        COURSE_BULK_CSV_INST_FNAME,
        COURSE_BULK_CSV_INST_LNAME,
        COURSE_BULK_CSV_INST_EMAIL,
        COURSE_BULK_CSV_INST_AUTH,
        COURSE_BULK_CSV_COURSE_NAME,
        COURSE_BULK_CSV_COURSE_SHORTNAME,
        COURSE_BULK_CSV_COURSE_CATEGORY
    ]


def course_bulk_outputput_csv_fieldnames():
    """Return array of fieldnames in output CSV for course bulk setup"""
    return [
        COURSE_BULK_CSV_INST_FNAME,
        COURSE_BULK_CSV_INST_LNAME,
        COURSE_BULK_CSV_INST_EMAIL,
        COURSE_BULK_CSV_INST_AUTH,
        COURSE_BULK_CSV_COURSE_NAME,
        COURSE_BULK_CSV_COURSE_SHORTNAME,
        COURSE_BULK_CSV_COURSE_CATEGORY,
        COURSE_BULK_CSV_COURSE_ID,
        COURSE_BULK_CSV_COURSE_ENROLMENT_URL,
        COURSE_BULK_CSV_COURSE_ENROLMENT_KEY
    ]


def setup_duplicate_course(
    moodle_client, base_course_id, coursedata, instructor_role_id,
    student_role_id
):
    """Setup a new course using a base and data from bulk CSV"""
    # Retrieve or create teacher account
    existing_user = moodle_client.get_user_by_email(
        coursedata[COURSE_BULK_CSV_INST_EMAIL]
    )
    if existing_user:
        instructor_user_id = existing_user['id']
    else:
        new_user = moodle_client.create_user(
            coursedata[COURSE_BULK_CSV_INST_FNAME],
            coursedata[COURSE_BULK_CSV_INST_LNAME],
            coursedata[COURSE_BULK_CSV_INST_EMAIL],
            coursedata[COURSE_BULK_CSV_INST_AUTH]
        )
        instructor_user_id = new_user["id"]

    # Create a duplicate course using the base course
    new_course = moodle_client.copy_course(
        base_course_id,
        coursedata[COURSE_BULK_CSV_COURSE_NAME],
        coursedata[COURSE_BULK_CSV_COURSE_SHORTNAME],
        coursedata[COURSE_BULK_CSV_COURSE_CATEGORY]
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
    coursedata[COURSE_BULK_CSV_COURSE_ID] = new_course_id
    coursedata[COURSE_BULK_CSV_COURSE_ENROLMENT_URL] = \
        moodle_client.get_course_enrolment_url(new_course_id)
    coursedata[COURSE_BULK_CSV_COURSE_ENROLMENT_KEY] = enrolment_key

    return coursedata
