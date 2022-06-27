<?php

defined('MOODLE_INTERNAL') || die();
require_once($CFG->libdir . '/externallib.php');
require_once($CFG->libdir . "/filelib.php");

class local_fe_events_direct_external extends external_api {

    public static function process_content_loaded_event_parameters() {
        return new external_function_parameters(
            array(
                  'contentId' => new external_value(PARAM_TEXT, 'Content ID')                )
            );
    }

    public static function process_content_loaded_event($contentid) {
        global $USER;

        $params = self::validate_parameters(
            self::process_content_loaded_event_parameters(),
            array('contentId' => $contentid)
        );

        self::validate_context(context_system::instance());

        $date = new DateTime();
        $data = [
            'eventname' => 'content_loaded',
            'user_id' => $USER->id,
            'content_id' => $contentid,
            'timestamp' => $date->getTimestamp()
        ];

        $jsondata = json_encode($data);
        $curl = new \curl();
        $options = array('CURLOPT_HTTPHEADER' => array('Content-Type:application/json'));
        $server = getenv('EVENTSAPI_SERVER');
        if ($server) {
            $response = $curl->post($server.'/events', $jsondata, $options);
        }

        return array();
    }

    public static function process_content_loaded_event_returns() {
        return new external_single_structure(
            array());
    }
}
