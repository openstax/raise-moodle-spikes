<?php

require_once("../../config.php");
require_once("$CFG->dirroot/mod/study/locallib.php");

$id = optional_param('id', 0, PARAM_INT);    // Course Module ID, or
$s = optional_param('s', 0, PARAM_INT);     // Study ID

if ($id) {
    $cm = get_coursemodule_from_id('study', $id, 0, false, MUST_EXIST);
    $study = $DB->get_record('study', array('id'=>$cm->instance), '*', MUST_EXIST);
} else {
    $study = $DB->get_record('study', array('id'=>$s), '*', MUST_EXIST);
    $cm = get_coursemodule_from_instance('study', $study->id, $study->course, false, MUST_EXIST);
}

$course = $DB->get_record('course', array('id'=>$cm->course), '*', MUST_EXIST);
require_course_login($course, true, $cm);

$PAGE->set_url('/mod/study/view.php', array('id' => $cm->id));
$pagetitle = $course->shortname.": ".$study->name;
$PAGE->set_title($pagetitle);
$PAGE->set_heading($course->shortname);

echo $OUTPUT->header();
echo $OUTPUT->heading(format_string($study->name), 2);
$cminfo = cm_info::create($cm);
$completiondetails = \core_completion\cm_completion_details::get_instance($cminfo, $USER->id);
$activitydates = \core\activity_dates::get_dates_for_module($cminfo, $USER->id);
echo $OUTPUT->activity_information($cminfo, $completiondetails, $activitydates);

if (trim(strip_tags($study->intro))) {
    echo $OUTPUT->box_start('mod_introbox', 'studyintro');
    echo format_module_intro('study', $study, $cm->id);
    echo $OUTPUT->box_end();
}

$research_id = get_or_create_research_id();
$encryptedtoken = generate_ssotoken($research_id, $study->secretkey);
$url = $study->studyurl.'?ssotoken='.$encryptedtoken;

echo <<<EOT
  <iframe src="$url" width="100%" height="600px"></iframe>
EOT;

echo $OUTPUT->footer();
