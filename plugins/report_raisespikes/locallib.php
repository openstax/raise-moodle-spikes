<?php


defined('MOODLE_INTERNAL') || die;

require_once(__DIR__.'/lib.php');
require_once($CFG->dirroot.'/course/lib.php');


function getLessonAttemptsData() {
    global $DB;

    $attemptsData = array();

    $table = 'lesson_attempts';

    $fields = 'id, lessonid, pageid, userid, answerid, retry, correct, useranswer, timeseen';

    $sql = "SELECT $fields FROM {" . $table . "}";

    $results = $DB->get_records_sql($sql);

    if (!empty($results)) {
        foreach ($results as $row) {
            $attemptsData[] = array(
                'id' => $row->id,
                'lessonid' => $row->lessonid,
                'pageid' => $row->pageid,
                'userid' => $row->userid,
                'answerid' => $row->answerid,
                'retry' => $row->retry,
                'correct' => $row->correct,
                'useranswer' => $row->useranswer,
                'timeseen' => $row->timeseen,
            );
        }
    }

    return $attemptsData;
}

function getLessonPageTitles($courseId) {
    global $DB;

    $lessonData = array();

    $table = 'lesson';

    $fields = 'id, name, course';

    $sql = "SELECT $fields FROM {" . $table . "} WHERE course = :courseid AND name NOT LIKE '%Teacher Guide%' ORDER BY id ASC";

    $params = array('courseid' => $courseId);

    $results = $DB->get_records_sql($sql, $params);

    if (!empty($results)) {
        foreach ($results as $row) {
            $lessonData[] = array(
                'id' => $row->id,
                'name' => $row->name,
                'course' => $row->course
            );
        }
    }

    return $lessonData;
}

