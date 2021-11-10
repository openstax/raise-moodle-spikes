<?php

defined('MOODLE_INTERNAL') || die;

function study_add_instance($data) {
    global $DB;

    $data->timemodified = time();
    $id = $DB->insert_record('study', $data);

    $completiontimeexpected = !empty($data->completionexpected) ? $data->completionexpected : null;
    \core_completion\api::update_completion_date_event($data->coursemodule, 'study', $id, $completiontimeexpected);

    return $id;
}

function study_update_instance($data) {
    global $DB;

    $data->timemodified = time();
    $data->id = $data->instance;

    $DB->update_record('study', $data);

    $completiontimeexpected = !empty($data->completionexpected) ? $data->completionexpected : null;
    \core_completion\api::update_completion_date_event($data->coursemodule, 'study', $data->id, $completiontimeexpected);

    return true;
}

function study_delete_instance($id) {
    global $DB;

    if (! $study = $DB->get_record('study', array('id'=>$id))) {
        return false;
    }

    $cm = get_coursemodule_from_instance('study', $id);
    \core_completion\api::update_completion_date_event($cm->id, 'study', $study->id, null);

    $DB->delete_records('study', array('id'=>$study->id));

    return true;
}
