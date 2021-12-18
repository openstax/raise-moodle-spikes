import pytest
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
    session_mock.post.return_value.json.return_value = {}
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


def test_get_courses(mocker):
    session_mock = mocker.Mock()
    session_mock.get.return_value.json.return_value = {}
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


def test_get_self_enrolment_methods(mocker):
    session_mock = mocker.Mock()
    session_mock.get.return_value.json.return_value = {}
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.get_self_enrolment_methods(111, 12)
    session_mock.get.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        params={
            "courseid": 111,
            "roleid": 12,
            "wsfunction": moodle.MOODLE_FUNC_GET_SELF_ENROLMENT_METHODS,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_get_role_by_shortname(mocker):
    session_mock = mocker.Mock()
    session_mock.get.return_value.json.return_value = {}
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.get_role_by_shortname("rolename")
    session_mock.get.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        params={
            "shortname": "rolename",
            "wsfunction": moodle.MOODLE_FUNC_GET_ROLE_BY_SHORTNAME,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_enable_self_enrolment_method(mocker):
    session_mock = mocker.Mock()
    session_mock.post.return_value.json.return_value = {}
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.enable_self_enrolment_method(111)
    session_mock.post.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        {
            "enrolid": 111,
            "wsfunction": moodle.MOODLE_FUNC_ENABLE_SELF_ENROLMENT_METHOD,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_set_self_enrolment_method_key(mocker):
    session_mock = mocker.Mock()
    session_mock.post.return_value.json.return_value = {}
    client = moodle.MoodleClient(
        session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN
    )
    client.set_self_enrolment_method_key(111, "Enrolment key value")
    session_mock.post.assert_called_once_with(
        f"{TEST_MOODLE_URL}{moodle.MOODLE_WEBSERVICE_PATH}",
        {
            "enrolid": 111,
            "enrolkey": "Enrolment key value",
            "wsfunction": moodle.MOODLE_FUNC_SET_SELF_ENROLMENT_METHOD_KEY,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )


def test_check_for_moodle_error(mocker):
    result_mock = mocker.Mock()
    result_mock.json.return_value = {
        "exception": "error"
    }

    with pytest.raises(Exception):
        moodle.check_for_moodle_error(result_mock)

    # Confirm we handle valid array responses without errors
    result_mock.json.return_value = []
    moodle.check_for_moodle_error(result_mock)
