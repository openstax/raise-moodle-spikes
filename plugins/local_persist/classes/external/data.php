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
            []
        );
    }

    public static function put_data() {
        $params = self::validate_parameters(
            self::put_data_parameters(),
            []
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
