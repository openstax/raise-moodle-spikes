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
$services = array(
      'FE Events (Direct) service' => array(
          'enabled' => 1,
          'shortname' => 'local_fe_events_direct_service',
          'functions' => array (
            'local_fe_events_direct_content_loaded_handler',
            'local_fe_events_direct_user_id_handler'
          ),
      ),
  );

  $functions = array(
    'local_fe_events_direct_content_loaded_handler' => array(
        'classname'   => 'local_fe_events_direct_external',
        'methodname'  => 'process_content_loaded_event',
        'description' => 'Sends event data directly to an EventsAPI and does not add them to the moodle database',
        'loginrequired' => true,
        'ajax' => true
    ),
    'local_fe_events_direct_user_id_handler' => array(
      'classname'   => 'local_fe_events_direct_external',
        'methodname'  => 'user_id',
        'description' => 'returns the requested userID if the request is internal',
        'loginrequired' => true,
        'ajax' => true
    )
  );
