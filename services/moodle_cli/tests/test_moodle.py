from moodlecli.moodle import MoodleClient, MOODLE_WEBSERVICE_PATH, \
    MOODLE_FUNC_COURSE_DUPLICATE

TEST_MOODLE_URL = "http://dagobah"
TEST_MOODLE_TOKEN = "1234"


def test_copy_course(mocker):
    session_mock = mocker.Mock()
    client = MoodleClient(session_mock, TEST_MOODLE_URL, TEST_MOODLE_TOKEN)
    client.copy_course(
        1,
        "Long name",
        "Short name",
        2
    )
    session_mock.post.assert_called_once_with(
        f"{TEST_MOODLE_URL}{MOODLE_WEBSERVICE_PATH}",
        {
            "courseid": 1,
            "fullname": "Long name",
            "shortname": "Short name",
            "categoryid": 2,
            "wsfunction": MOODLE_FUNC_COURSE_DUPLICATE,
            "moodlewsrestformat": "json",
            "wstoken": TEST_MOODLE_TOKEN
        }
    )
