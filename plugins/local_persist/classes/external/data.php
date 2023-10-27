<?php

namespace local_persist\external;

defined('MOODLE_INTERNAL') || die();

use external_api;
use external_function_parameters;
use external_value;
use external_single_structure;
use external_multiple_structure;

class data extends external_api {

    public static function put_data_parameters() {
        return new external_function_parameters(
            [
                "courseid" => new external_value(PARAM_TEXT, 'Course ID associated with this data'),
                "prefetchKey" => new external_value(PARAM_TEXT, 'Prefetch key', VALUE_DEFAULT, null),
                "key" => new external_value(PARAM_TEXT, 'Data key'),
                "value" => new external_value(PARAM_RAW, 'Data value')
            ]
        );
    }

    public static function put_data($courseid, $prefetchKey, $key, $value) {
        global $USER, $DB;

        $params = self::validate_parameters(
            self::put_data_parameters(),
            ['courseid' => $courseid, 'prefetchKey' => $prefetchKey, 'key' => $key, 'value' => $value]
        );

        $existingdata = $DB->get_record(
            'local_persist_data',
            ['user_id' => $USER->id, 'course_id' => $params['courseid'], 'prefetch_key' => $params['prefetchKey'], 'data_key' => $params['key']],
            'id,user_id,course_id,prefetch_key,data_key',
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
                'prefetch_key' => $params['prefetchKey'],
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

    public static function get_data_parameters() {
        return new external_function_parameters(
            [
                "courseid" => new external_value(PARAM_TEXT, 'Course ID associated with this data'),
                "prefetchKey" => new external_value(PARAM_TEXT, 'Prefetch key', VALUE_DEFAULT, null),
                "key" => new external_value(PARAM_TEXT, 'Data key')
            ]
        );
    }

    public static function get_data($courseid, $prefetchKey, $key) {
        global $USER, $DB;

        $params = self::validate_parameters(
            self::get_data_parameters(),
            ['courseid' => $courseid, 'prefetchKey' => $prefetchKey, 'key' => $key]
        );

        $data_test = $DB->get_recordset(
            'local_persist_data',
            ['user_id' => $USER->id, 'course_id' => $params['courseid'], 'prefetch_key' => $params['prefetchKey'], 'data_key' => $params['key']],
            '',
            'data_key, data_value'
        );

        $data = [];
        // This is the implementation portion. If prefetch_key exists then prefetch query, otherwise query like we
        // were previously doing.
        if ($data_test->valid()) {
            foreach ($data_test as $item) {
                $data[] = [
                    "key" => $item->data_key,
                    "value" => $item->data_value
                ];
            }
        }

        $data_test->close();    
        return $data;
    }

    public static function get_data_returns() {
        return new external_multiple_structure(
            new external_single_structure(
                [
                    "key" => new external_value(PARAM_TEXT, 'Data key'),
                    "value" => new external_value(PARAM_RAW, 'Data value')
                ]
            )
        );
    }
}
