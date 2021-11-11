<?php

defined('MOODLE_INTERNAL') || die();

if ($hassiteconfig) {
    $ADMIN->add(
        'tools',
        new admin_category(
            'tool_events',
            new lang_string('pluginname', 'tool_events')
        )
    );
}
