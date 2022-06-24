<?php

defined('MOODLE_INTERNAL') || die();

$services = array(
      'directeventhandler' => array(                                                // the name of the web service
          'functions' => array ('local_direct_event_handler'), // web service functions of this service
          'requiredcapability' => '',                // if set, the web service user need this capability to access 
                                                                              // any function of this service. For example: 'some/capability:specified'                 
          'restrictedusers' => 0,                                             // if enabled, the Moodle administrator must link some user to this service
                                                                              // into the administration
          'enabled' => 1,                                                       // if enabled, the service can be reachable on a default installation
          'shortname' =>  'd_handler',       // optional – but needed if restrictedusers is set so as to allow logins.
          'downloadfiles' => 0,    // allow file downloads.
          'uploadfiles'  => 0,      // allow file uploads.
          'ajax' => true
       )
  );

  $functions = array(
    'local_direct_event_handler' => array(         //web service function name
        'classname'   => 'local_direct_external',  //class containing the external function OR namespaced class in classes/external/XXXX.php
        'methodname'  => 'process_event',          //external function name                                                   // defaults to the service's externalib.php
        'description' => 'Sends event data to the API Endpoint',    //human readable description of the web service function
        'type'        => 'write',                  //database rights of the web service function (read, write)
        'ajax' => true,        // is the service available to 'internal' ajax calls.  'services'=> // Optional, only available for Moodle 3.1 onwards. List of built-in services (by shortname) where the function will be included.  Services created manually via the Moodle interface are not supported.
        'capabilities' => '', // comma separated list of capabilities used by the function.
    ),
);