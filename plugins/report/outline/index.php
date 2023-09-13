<?php


use core\report_helper;

require('../../config.php');
require_once($CFG->dirroot.'/report/outline/locallib.php');

$id = required_param('id',PARAM_INT);       // course id
$startdate = optional_param('startdate', null, PARAM_INT);
$enddate = optional_param('enddate', null, PARAM_INT);

$course = $DB->get_record('course', array('id'=>$id), '*', MUST_EXIST);

$pageparams = array('id' => $id);
if ($startdate) {
    $pageparams['startdate'] = $startdate;
}
if ($enddate) {
    $pageparams['enddate'] = $enddate;
}

$PAGE->set_url('/report/outline/index.php', $pageparams);
$PAGE->set_pagelayout('report');

require_login($course);
$context = context_course::instance($course->id);
require_capability('report/outline:view', $context);


// Trigger an activity report viewed event.
$event = \report_outline\event\activity_report_viewed::create(array('context' => $context));
$event->trigger();

$showlastaccess = true;
$hiddenfields = explode(',', $CFG->hiddenuserfields);

if (array_search('lastaccess', $hiddenfields) !== false and !has_capability('moodle/user:viewhiddendetails', $context)) {
    $showlastaccess = false;
}

$stractivityreport = get_string('pluginname', 'report_outline');
$stractivity       = get_string('activity');

$PAGE->set_title($course->shortname .': '. $stractivityreport);
$PAGE->set_heading($course->fullname);
echo $OUTPUT->header();

// Print selector drop down.
$pluginname = get_string('pluginname', 'report_outline');
report_helper::print_report_selector($pluginname);

$getLessonGradesData = getLessonGradesData();
$pageTitles = getLessonPageTitles();
$attemptsData = getLessonAttemptsData();

$table = new html_table();
$table->head = array_merge(['Lesson'], array_unique(array_column($attemptsData, 'userid')));

$lessonAttempts = array();

$userIds = array_unique(array_column($attemptsData, 'userid'));
// filter by courseid
foreach ($userIds as $userId) {
    foreach ($pageTitles as $lessonData) {
        $lessonId = $lessonData['lessonid'];
        $lessonAttempts[$lessonId][$userId] = false;
    }
}

// Loop through attempts data and update user attempts as true where necessary.
foreach ($attemptsData as $attempt) {
    $lessonId = $attempt['lessonid'];
    $userId = $attempt['userid'];

    $lessonAttempts[$lessonId][$userId] = true;
}

// Populate the table with data.
foreach ($pageTitles as $lessonData) {
    $lessonId = $lessonData['lessonid'];
    $lessonTitle = $lessonData['title'];

    $row = array($lessonTitle);

    foreach ($userIds as $userId) {
        $row[] = isset($lessonAttempts[$lessonId][$userId]) && $lessonAttempts[$lessonId][$userId] ? 'True' : 'False';
    }

    $table->data[] = $row;
}

// Render the table.
echo html_writer::table($table);

// Add a footer to your page (optional).
echo $OUTPUT->footer();
