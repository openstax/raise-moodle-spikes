MOODLE_WEBSERVICE_PATH = "/webservice/rest/server.php"

MOODLE_FUNC_GET_COURSES = "core_course_get_courses"
MOODLE_FUNC_DUPLICATE_COURSE = "core_course_duplicate_course"
MOODLE_FUNC_GET_COURSE_ENROLMENT_METHODS = \
    "core_enrol_get_course_enrolment_methods"
MOODLE_FUNC_ENROL_SELF_INSTANCE_INFO = "enrol_self_get_instance_info"
MOODLE_FUNC_ENABLE_SELF_ENROLMENT_METHOD = \
    "local_raisecli_enable_self_enrolment_method"
MOODLE_FUNC_GET_ROLE_BY_SHORTNAME = "local_raisecli_get_role_by_shortname"
MOODLE_FUNC_GET_SELF_ENROLMENT_METHODS = \
    "local_raisecli_get_self_enrolment_methods"
MOODLE_FUNC_SET_SELF_ENROLMENT_METHOD_KEY = \
    "local_raisecli_set_self_enrolment_method_key"


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

    def _create_params(self, service_function, data):
        params = {
            "wsfunction": service_function,
            "moodlewsrestformat": "json",
            "wstoken": self.token
        }
        if data:
            params.update(convert_moodle_params(data))
        return params

    def _post(self, service_function, data):
        """POST to service function with provided data as parameters"""
        res = self.session.post(
            self.service_endpoint,
            self._create_params(service_function, data)
        )

        res.raise_for_status()
        return res.json()

    def _get(self, service_function, data=None):
        """GET to service function with provided data as parameters"""
        res = self.session.get(
            self.service_endpoint,
            params=self._create_params(service_function, data)
        )

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
        return self._post(
            MOODLE_FUNC_DUPLICATE_COURSE,
            data
        )

    def get_self_enrolment_info(self, enrolment_id):
        data = {
            "instanceid": enrolment_id
        }
        return self._get(
            MOODLE_FUNC_ENROL_SELF_INSTANCE_INFO,
            data
        )

    def get_courses(self):
        return self._get(MOODLE_FUNC_GET_COURSES)

    def get_course_enrolment_methods(self, course_id):
        data = {
            "courseid": course_id
        }
        return self._get(MOODLE_FUNC_GET_COURSE_ENROLMENT_METHODS, data)

    def get_self_enrolment_methods(self, course_id, role_id):
        data = {
            "courseid": course_id,
            "roleid": role_id
        }
        return self._get(MOODLE_FUNC_GET_SELF_ENROLMENT_METHODS, data)

    def get_role_by_shortname(self, shortname):
        data = {
            "shortname": shortname
        }
        return self._get(MOODLE_FUNC_GET_ROLE_BY_SHORTNAME, data)

    def enable_self_enrolment_method(self, enrol_id):
        data = {
            "enrolid": enrol_id
        }
        return self._post(MOODLE_FUNC_ENABLE_SELF_ENROLMENT_METHOD, data)

    def set_self_enrolment_method_key(self, enrol_id, enrol_key):
        data = {
            "enrolid": enrol_id,
            "enrolkey": enrol_key
        }
        return self._post(MOODLE_FUNC_SET_SELF_ENROLMENT_METHOD_KEY, data)
