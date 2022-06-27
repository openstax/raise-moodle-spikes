<?php

defined('MOODLE_INTERNAL') || die();
$services = array(
      'directeventhandler' => array(
          'functions' => array ('local_fe_events_direct_content_loaded_handler'),
          'enabled' => 1,
          'shortname' => 'local_fe_events_direct_service'
       )
  );

  $functions = array(
    'local_fe_events_direct_content_loaded_handler' => array(
        'classname'   => 'local_fe_events_direct_external',
        'methodname'  => 'process_content_loaded_event',
        'description' => 'Sends event data directly to an EventsAPI and does not add them to the moodle database',
        'loginrequired' => true,
        'ajax' => true
    ),
  );
