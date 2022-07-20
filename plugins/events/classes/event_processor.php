<?php

namespace tool_events;

defined('MOODLE_INTERNAL') || die();

class event_processor {
    public static function process_event(\core\event\base $event) {
        global $DB;

        // Filter event if userid is <=0 (not logged in or system)
        if ($event->userid <= 0)
            return;

        // Prepare event data if an event we're tracking and otherwise return
        switch ($event->eventname) {
            // Notable shortcuts:
            // * Generating event in sync vs queueing for async processing
            // * There are a lot of queries here, many of which are for easily
            //   cacheable data.
            case '\\mod_lesson\\event\\content_page_viewed':
                $eventdata = $event->get_data();
                $username = $DB->get_field('user', 'username', ['id' => $eventdata['userid']]);
                $timestamp = $eventdata['timecreated'];
                $coursename = $DB->get_field('course', 'fullname', ['id' => $eventdata['courseid']]);
                $lessonpage = $DB->get_record(
                    $eventdata['objecttable'],
                    ['id' => $eventdata['objectid']],
                    'title,lessonid'
                );
                $pagetitle = $lessonpage->title;
                $lessonname = $DB->get_field(
                    'lesson',
                    'name',
                    ['id' => $lessonpage->lessonid]
                );
                $data = [
                    'username' => $username,
                    'eventname' => $event->eventname,
                    'timestamp' => $timestamp,
                    'course_name' => $coursename,
                    'page_title' => $pagetitle,
                    'lesson_name' => $lessonname
                ];
                break;
            case '\\core\\event\\user_graded':
                $eventdata = $event->get_data();
                $username = $DB->get_field('user', 'username', ['id' => $eventdata['userid']]);
                $timestamp = $eventdata['timecreated'];
                $coursename = $DB->get_field('course', 'fullname', ['id' => $eventdata['courseid']]);
                $lessonname = $DB->get_field(
                    'grade_items',
                    'itemname',
                    ['id' => $eventdata['other']['itemid']]
                );
                $data = [
                    'username' => $username,
                    'eventname' => $event->eventname,
                    'timestamp' => $timestamp,
                    'course_name' => $coursename,
                    'lesson_name' => $lessonname,
                    'grade' => $eventdata['other']['finalgrade']
                ];
                break;
                case '\\local_fe_events_moodle\\event\\fe_event':
                    $eventdata = $event->get_data();
                    $username = $DB->get_field('user', 'username', ['id' => $eventdata['userid']]);
                    $timestamp = $eventdata['timecreated'];
                    $coursename = $DB->get_field('course', 'fullname', ['id' => $eventdata['courseid']]);
                    $lessonname = $DB->get_field(
                        'grade_items',
                        'itemname',
                        ['id' => $eventdata['other']['itemid']]
                    );
                    $data = [
                        'eventname' => 'EVENT NAME',
                        'user_id' => 'USERID' ,
                        'content_id' => 'CONTENT_ID',
                        'timestamp' => '$date->getTimestamp()'
                    ];
                    break;
            default:
                return;
        }

        $jsondata = json_encode($data);
        $curl = new \curl();
        $options = array('CURLOPT_HTTPHEADER' => array('Content-Type:application/json'));
        $server = getenv('EVENTSAPI_SERVER');
        if ($server) {
            $curl->post($server.'/events', $jsondata, $options);
        }
    }
}
