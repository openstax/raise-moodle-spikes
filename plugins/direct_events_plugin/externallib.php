<?php

require_once($CFG->libdir . '/externallib.php');
require_once($CFG->libdir . "/filelib.php");

defined('MOODLE_INTERNAL') || die();

class local_direct_external extends external_api {

    public static function process_event_parameters(){
        return new external_function_parameters(
            array(
                  'content_id' => new external_value(PARAM_TEXT, 'Content ID')                )
            );
    }

    public static function process_event($content_id) {
        global $USER; 

        $params = self::validate_parameters(
            self::process_event_parameters(),
            array('content_id' => $content_id)
        );

        self::validate_context(context_system::instance());

        $date = new DateTime();
        $data = [
            'eventname' => 'content_loaded',
            'user_id' => $USER->id,
            'content_id' => $content_id,
            'timestamp' => $date->getTimestamp()
        ];

        $jsondata = json_encode($data);
        $curl = new \curl();
        $options = array('CURLOPT_HTTPHEADER' => array('Content-Type:application/json'));
        $server = getenv('EVENTSAPI_SERVER');
        if ($server) {
            $response = $curl->post($server.'/events', $jsondata, $options);
        }

        return array(
            "confirm" => $response
        );
    }

    public static function process_event_returns(){
        return new external_single_structure(
            array(
                'confirm' => new external_value(PARAM_TEXT, 'Whether the event was received or not')
            )
        );
    }
}