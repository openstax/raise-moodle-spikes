<?php


defined('MOODLE_INTERNAL') || die;

require_once(__DIR__.'/lib.php');
require_once($CFG->dirroot.'/course/lib.php');

function getLessonGradesData() {
    global $DB;

    $gradesData = array();

    $table = 'lesson_grades';

    $fields = 'id, lessonid, userid, grade, late, completed';

    $sql = "SELECT $fields FROM {" . $table . "}";

    $results = $DB->get_records_sql($sql);

    if (!empty($results)) {
        foreach ($results as $row) {
            $gradesData[] = array(
                'id' => $row->id,
                'lessonid' => $row->lessonid,
                'userid' => $row->userid,
                'grade' => $row->grade,
                'late' => $row->late,
                'completed' => $row->completed,
            );
        }
    }

    return $gradesData;
}

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

function getLessonPageTitles() {
    global $DB;

    $lessonData = array();

    $table = 'lesson_pages';

    $fields = 'lessonid, title';

    $sql = "SELECT $fields FROM {" . $table . "}";

    $results = $DB->get_records_sql($sql);

    if (!empty($results)) {
        foreach ($results as $row) {
            $lessonData[] = array(
                'lessonid' => $row->lessonid,
                'title' => $row->title,
            );
        }
    }

    return $lessonData;
}

