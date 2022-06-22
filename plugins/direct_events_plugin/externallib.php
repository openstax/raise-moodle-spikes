<?php

require_once("$CFG->libdir/externallib.php");

defined('MOODLE_INTERNAL') || die();

class local_direct_sender extends external_api {

    public static function process_event_parameters(){
        return new external_function_parameters(
            array(
                    'event_id' => new external_value(PARAM_TEXT, 'Event ID'),
                    'event_description' => new external_value(PARAM_TEXT, 'Event Description')
                )
            );
    }

    public static function process_event($event_id, $event_description) {
        global $DB;

        $params = self::validate_parameters(
            self::process_event_parameters(),
            array('event_id' => $event_id,
                  'event_description' => $event_description)
        );

        self::validate_context(context_system::instance());

        $timestamp = "0:00";
        $data = [
            'event_id' => $event_id,
            'timestamp' => $timestamp,
            'event_description' => $event_description
        ];

        $jsondata = json_encode($data);
        $curl = new \curl();
        $options = array('CURLOPT_HTTPHEADER' => array('Content-Type:application/json'));
        $server = getenv('EVENTSAPI_SERVER');
        if ($server) {
            $curl->post($server.'/events', $jsondata, $options);
        }

        return array(
            "confirm" => "event id is ".$event_id." description: ".$event_description
        );
    }

    public static function process_event_returns(){
        return new external_single_structure(
            array(
                'confirm' => new external_value(PARAM_TEXT, 'The return confimation')
            )
        );
    }
}