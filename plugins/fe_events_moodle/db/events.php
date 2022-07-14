<?php

defined('MOODLE_INTERNAL') || die();

// List of observers.
$observers = array(
    array(
        'eventname'   => '*',
        'callback'    => '\fe_events_moodle\event_processor::process_event',
    ),
);