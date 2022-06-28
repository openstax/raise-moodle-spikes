<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Plugin version and other metadata.
 *
 * @package    local_fe_events_direct
 * @copyright  2021 OpenStax
 * @license    https://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
defined('MOODLE_INTERNAL') || die();
require_once($CFG->libdir . '/externallib.php');
require_once($CFG->libdir . "/filelib.php");

/**
 * Front End Events Direct Web Service
 *
 * @package    local_fe_events_direct
 * @copyright  2021 OpenStax
 * @license    https://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class local_fe_events_direct_external extends external_api {

    /**
     * Returns description of process_content_loaded_event() parameters
     *
     * @return external_function_parameters
     */
    public static function process_content_loaded_event_parameters() {
        return new external_function_parameters(
            array(
                  'contentId' => new external_value(PARAM_TEXT, 'Content ID')                )
            );
    }

    /**
     * Forward content_loaded event to EventsAPI.
     *
     * @param str $contentid
     * @return array empty array
     */
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

    /**
     * Returns description of process_content_loaded_event() result value
     *
     * @return external_description
     */
    public static function process_content_loaded_event_returns() {
        return new external_single_structure(
            array());
    }
}
