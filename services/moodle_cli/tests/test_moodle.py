from moodlecli import moodle

TEST_MOODLE_URL = "http://dagobah"
TEST_MOODLE_TOKEN = "1234"


def test_convert_moodle_params():
    cases = [
        {
            "input": {"a": 1, "b": 2},
            "expected": {"a": 1, "b": 2}
        },
        {
            "input": {"foo": [{"a": 1, "b": 2}, {"a": 3, "b": 4}]},
            "expected": {
                "foo[0][a]": 1,
                "foo[0][b]": 2,
                "foo[1][a]": 3,
                "foo[1][b]": 4,
            }
        }
    ]
    for case in cases:
        assert moodle.convert_moodle_params(case["input"]) == case["expected"]


def test_copy_course(mocker):
    session_mock = mocker.Mock()
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.copy_course(
        1,
        "Long name",
        "Short name",
        2
    )
    session_mock.post.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        {
            "courseid": 1,
            "fullname": "Long name",
            "shortname": "Short name",
            "categoryid": 2,
            "wsfunction": moodle.MOODLE_FUNC_DUPLICATE_COURSE,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_self_enrolment_info(mocker):
    session_mock = mocker.Mock()
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.get_self_enrolment_info(111)
    session_mock.get.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        params={
            "instanceid": 111,
            "wsfunction": moodle.MOODLE_FUNC_ENROL_SELF_INSTANCE_INFO,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_get_courses(mocker):
    session_mock = mocker.Mock()
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.get_courses()
    session_mock.get.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        params={
            "wsfunction": moodle.MOODLE_FUNC_GET_COURSES,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_get_course_enrolment_methods(mocker):
    session_mock = mocker.Mock()
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.get_course_enrolment_methods(111)
    session_mock.get.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        params={
            "courseid": 111,
            "wsfunction": moodle.MOODLE_FUNC_GET_COURSE_ENROLMENT_METHODS,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )
