<?php

defined('MOODLE_INTERNAL') || die();

  $functions = [
    'local_persist_put' => [
        'classname'   => 'local_persist\external\data',
        'methodname'  => 'put_data',
        'description' => 'Store data for RAISE',
        'loginrequired' => true,
        'ajax' => true
    ],
    'local_persist_get' => [
      'classname'   => 'local_persist\external\data',
      'methodname'  => 'get_data',
      'description' => 'Get data for RAISE',
      'loginrequired' => true,
      'ajax' => true
  ]
  ];
