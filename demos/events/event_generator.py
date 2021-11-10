import json
import uuid
import random

NUM_STUDENTS = 100
PROB_ACTIVITY1 = 0.5
PROB_PASS_ACTIVITY1 = 0.75
PROB_PASS_ACTIVITY2 = 0.25

BASE_GRADED_EVENT = {
    "username": "",
    "eventname": "\\core\\event\\user_graded",
    "timestamp": 1630705789,
    "course_name": "RAISE Algebra 1",
    "lesson_name": "Demo lesson",
    "grade": ""
}

BASE_START_EVENT = {
    "username": "",
    "eventname": "\\mod_lesson\\event\\content_page_viewed",
    "timestamp": 1630705775,
    "course_name": "RAISE Algebra 1",
    "page_title": "Starting content",
    "lesson_name": "Demo lesson"
}

BASE_ACTIVITY1_EVENT = {
    "username": "",
    "eventname": "\\mod_lesson\\event\\content_page_viewed",
    "timestamp": 1630705783,
    "course_name": "RAISE Algebra 1",
    "page_title": "PHET activity",
    "lesson_name": "Demo lesson"
}

BASE_ACTIVITY2_EVENT = {
    "username": "",
    "eventname": "\\mod_lesson\\event\\content_page_viewed",
    "timestamp": 1630705783,
    "course_name": "RAISE Algebra 1",
    "page_title": "Desmos activity",
    "lesson_name": "Demo lesson"
}

for student_id in range(NUM_STUDENTS):
    username = f"user{student_id}"
    selected_activity1 = False
    if random.random() < PROB_ACTIVITY1:
        activity_event = BASE_ACTIVITY1_EVENT
        selected_activity1 = True
    else:
        activity_event = BASE_ACTIVITY2_EVENT
    activity_event["username"] = username
    start_event = BASE_START_EVENT
    start_event["username"] = username
    grade_event = BASE_GRADED_EVENT
    grade_event["username"] = username

    random_pass = random.random()
    should_pass = \
        (selected_activity1 and random_pass < PROB_PASS_ACTIVITY1) or \
        (not selected_activity1 and random_pass < PROB_PASS_ACTIVITY2)
    if should_pass:
        grade_event["grade"] = "100.0"
    else:
        grade_event["grade"] = "0.0"

    for event in [start_event, activity_event, grade_event]:
        output_filename = f"{uuid.uuid4()}.json"
        with open(output_filename, "w") as outfile:
            json.dump(event, outfile)
