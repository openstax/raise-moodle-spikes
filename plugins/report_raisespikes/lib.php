<?php


defined('MOODLE_INTERNAL') || die;

/**
 * This function extends the course navigation with the report items
 *
 * @param navigation_node $navigation The navigation node to extend
 * @param stdClass $course The course to object for the report
 * @param stdClass $context The context of the course
 */
function report_raisespikes_extend_navigation_course($navigation, $course, $context) {
    if (has_capability('report/raisespikes:view', $context)) {
        $url = new moodle_url('/report/raisespikes/index.php', array('id'=>$course->id));
        $navigation->add(get_string('pluginname', 'report_raisespikes'), $url, navigation_node::TYPE_SETTING, null, null, new pix_icon('i/report', ''));
    }
}

