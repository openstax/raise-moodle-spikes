<?php

namespace local_persist\external;

defined('MOODLE_INTERNAL') || die();

use external_api;
use external_function_parameters;
use external_value;
use external_single_structure;

class data extends external_api {

    public static function put_data_parameters() {
        return new external_function_parameters(
            [
                "courseid" => new external_value(PARAM_TEXT, 'Course ID associated with this data'),
                "key" => new external_value(PARAM_TEXT, 'Key to store / query data'),
                "value" => new external_value(PARAM_TEXT, 'Data to store')
            ]
        );
    }

    public static function put_data($courseid, $key, $value) {
        global $USER, $DB;

        $params = self::validate_parameters(
            self::put_data_parameters(),
            ['courseid' => $courseid, 'key' => $key, 'value' => $value]
        );

        $existingdata = $DB->get_record(
            'local_persist_data',
            ['user_id' => $USER->id, 'course_id' => $params['courseid'], 'data_key' => $params['key']],
            'id,user_id,course_id,data_key',
            IGNORE_MISSING
        );

        if ($existingdata) {
            $existingdata->data_value = $params['value'];
            $DB->update_record(
                'local_persist_data',
                $existingdata
            );
        } else {
            $newdata = [
                'user_id' => $USER->id,
                'course_id' => $params['courseid'],
                'data_key' => $params['key'],
                'data_value' => $params['value']
            ];

            $DB->insert_record(
                'local_persist_data',
                $newdata
            );
        }

        return [
        ];
    }

    public static function put_data_returns() {
        return new external_single_structure(
            [
            ]
        );
    }
}
