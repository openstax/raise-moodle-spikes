<?php

defined('MOODLE_INTERNAL') || die();

// List of observers.
$observers = array(
    array(
        'eventname'   => '*',
        'callback'    => '\tool_events\event_processor::process_event',
    ),
);