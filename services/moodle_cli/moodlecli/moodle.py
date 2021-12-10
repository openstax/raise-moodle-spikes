MOODLE_WEBSERVICE_PATH = "/webservice/rest/server.php"
MOODLE_FUNC_COURSE_DUPLICATE = "core_course_duplicate_course"


def convert_moodle_params(data, prefix=""):
    """Given a dict / array, convert into a flat dict that Moodle expects
    where the key names define the structure.
    """
    result = {}

    if not isinstance(data, (list, dict)):
        result[prefix] = data
        return result

    if not prefix:
        prefix = "{0}"
    else:
        prefix += "[{0}]"

    if isinstance(data, list):
        for idx, val in enumerate(data):
            elem_data = convert_moodle_params(
                val,
                prefix.format(idx)
            )
            result.update(elem_data)
    elif isinstance(data, dict):
        for key, val in data.items():
            elem_data = convert_moodle_params(
                val,
                prefix.format(key)
            )
            result.update(elem_data)

    return result


class MoodleClient:
    def __init__(self, session, moodle_url, moodle_token):
        self.session = session
        self.service_endpoint = f"{moodle_url}{MOODLE_WEBSERVICE_PATH}"
        self.token = moodle_token

    def post(self, service_function, data):
        """POST to service function with provided data as parameters"""
        params = {
            "wsfunction": service_function,
            "moodlewsrestformat": "json",
            "wstoken": self.token
        }
        params.update(convert_moodle_params(data))

        res = self.session.post(self.service_endpoint, params)

        res.raise_for_status()
        return res.json()

    def copy_course(
        self, source_id, course_name, course_shortname, course_category_id
    ):
        data = {
            "courseid": source_id,
            "fullname": course_name,
            "shortname": course_shortname,
            "categoryid": course_category_id
        }
        return self.post(
            MOODLE_FUNC_COURSE_DUPLICATE,
            data
        )
