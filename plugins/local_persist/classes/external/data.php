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
                "courseId" => new external_value(PARAM_TEXT, 'Course ID associated with this data'),
                "prefetchKey" => new external_value(PARAM_TEXT, 'Prefetch key', VALUE_DEFAULT, null),
                "dataKey" => new external_value(PARAM_TEXT, 'Data key'),
                "dataValue" => new external_value(PARAM_RAW, 'Data value')
            ]
        );
    }

    public static function put_data($courseId, $prefetchKey, $dataKey, $dataValue) {
        global $USER, $DB;

        $params = self::validate_parameters(
            self::put_data_parameters(),
            ['courseId' => $courseId, 'prefetchKey' => $prefetchKey, 'dataKey' => $dataKey, 'dataValue' => $dataValue]
        );

        $existingdata = $DB->get_record(
            'local_persist_data',
            ['user_id' => $USER->id, 'course_id' => $params['courseId'], 'data_key' => $params['dataKey']],
            'id,user_id,course_id,prefetch_key,data_key',
            IGNORE_MISSING
        );

        if ($existingdata) {
            $existingdata->data_value = $params['dataValue'];
            $existingdata->prefetch_key = $params['prefetchKey'];
            $DB->update_record(
                'local_persist_data',
                $existingdata
            );
        } else {
            $newdata = [
                'user_id' => $USER->id,
                'course_id' => $params['courseId'],
                'prefetch_key' => $params['prefetchKey'],
                'data_key' => $params['dataKey'],
                'data_value' => $params['dataValue']
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
                "courseId" => new external_value(PARAM_TEXT, 'Course ID associated with this data'),
                "prefetchKey" => new external_value(PARAM_TEXT, 'Prefetch key', VALUE_DEFAULT, null),
                "dataKey" => new external_value(PARAM_TEXT, 'Data key', VALUE_DEFAULT, null)
            ]
        );
    }

    public static function get_data($courseId, $prefetchKey, $dataKey) {
        global $USER, $DB;

        $params = self::validate_parameters(
            self::get_data_parameters(),
            ['courseId' => $courseId, 'prefetchKey' => $prefetchKey, 'dataKey' => $dataKey]
        );

        if ($prefetchKey) {
            $prefetch_data = $DB->get_recordset(
                'local_persist_data',
                ['user_id' => $USER->id, 'course_id' => $params['courseId'], 'prefetch_key' => $params['prefetchKey']],
                '',
                'data_key, data_value'
            );
        } else {
            $prefetch_data = $DB->get_recordset(
                'local_persist_data',
                ['user_id' => $USER->id, 'course_id' => $params['courseId'], 'data_key' => $params['dataKey']],
                '',
                'data_key, data_value'
            );
        }

        $data = [];
        if ($prefetch_data->valid()) {
            foreach ($prefetch_data as $item) {
                $data[] = [
                    "dataKey" => $item->data_key,
                    "dataValue" => $item->data_value
                ];
            }
        }

        $prefetch_data->close();    
        return $data;
    }

    public static function get_data_returns() {
        return new external_multiple_structure(
            new external_single_structure(
                [
                    "dataKey" => new external_value(PARAM_TEXT, 'Data key'),
                    "dataValue" => new external_value(PARAM_RAW, 'Data value')
                ]
            )
        );
    }
}
