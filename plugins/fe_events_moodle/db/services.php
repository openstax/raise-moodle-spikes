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
 * @package    local_fe_events_moodle
 * @copyright  2021 OpenStax
 * @license    https://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
defined('MOODLE_INTERNAL') || die();
$services = array(
      'FE Events moodle service' => array(
          'functions' => array ('local_fe_events_moodle_content_loaded_handler'),
          'enabled' => 1,
          'shortname' => 'local_fe_events_moodle_service'
       )
  );

  $functions = array(
    'local_fe_events_moodle_content_loaded_handler' => array(
        'classname'   => 'local_fe_events_moodle_external',
        'methodname'  => 'process_content_loaded_event',
        'description' => 'Sends event data directly to moodle via a new event',
        'loginrequired' => true,
        'ajax' => true
    ),
  );
