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
        $params = self::validate_parameters(
            self::put_data_parameters(),
            ['courseid' => $courseid, 'key' => $key, 'value' => $value]
        );

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
