<?php
/**
 * This script is a slightly modified version of the original script in the
 * Moodle codebase admin/cli/backup.php. The changes here create backups
 * without user data.
 */

define('CLI_SCRIPT', 1);

require('/var/www/html/config.php');
require_once($CFG->libdir.'/clilib.php');
require_once($CFG->dirroot . '/backup/util/includes/backup_includes.php');

// Now get cli options.
list($options, $unrecognized) = cli_get_params(array(
    'courseid' => false,
    'courseshortname' => '',
    'destination' => '',
    'help' => false,
    ), array('h' => 'help'));

if ($unrecognized) {
    $unrecognized = implode("\n  ", $unrecognized);
    cli_error(get_string('cliunknowoption', 'admin', $unrecognized));
}

if ($options['help'] || !($options['courseid'] || $options['courseshortname'])) {
    $help = <<<EOL
Perform backup of the given course.

Options:
--courseid=INTEGER          Course ID for backup.
--courseshortname=STRING    Course shortname for backup.
--destination=STRING        Path where to store backup file. If not set the backup
                            will be stored within the course backup file area.
-h, --help                  Print out this help.

Example:
\$sudo -u www-data /usr/bin/php admin/cli/backup.php --courseid=2 --destination=/moodle/backup/\n
EOL;

    echo $help;
    die;
}

$admin = get_admin();
if (!$admin) {
    mtrace("Error: No admin account was found");
    die;
}

// Do we need to store backup somewhere else?
$dir = rtrim($options['destination'], '/');
if (!empty($dir)) {
    if (!file_exists($dir) || !is_dir($dir) || !is_writable($dir)) {
        mtrace("Destination directory does not exists or not writable.");
        die;
    }
}

// Check that the course exists.
if ($options['courseid']) {
    $course = $DB->get_record('course', array('id' => $options['courseid']), '*', MUST_EXIST);
} else if ($options['courseshortname']) {
    $course = $DB->get_record('course', array('shortname' => $options['courseshortname']), '*', MUST_EXIST);
}

cli_heading('Performing backup...');
$bc = new backup_controller(backup::TYPE_1COURSE, $course->id, backup::FORMAT_MOODLE,
                            backup::INTERACTIVE_YES, backup::MODE_GENERAL, $admin->id);
// Set the default filename.
$bc->get_plan()->get_setting('users')->set_value('0');
$bc->get_plan()->get_setting('files')->set_value('1');
$bc->get_plan()->get_setting('filters')->set_value('0');
$bc->get_plan()->get_setting('calendarevents')->set_value('0');
$bc->get_plan()->get_setting('groups')->set_value('0');
$bc->get_plan()->get_setting('competencies')->set_value('0');
$bc->get_plan()->get_setting('customfield')->set_value('0');
$bc->get_plan()->get_setting('contentbankcontent')->set_value('0');
$bc->get_plan()->get_setting('legacyfiles')->set_value('0');
$format = $bc->get_format();
$type = $bc->get_type();
$id = $bc->get_id();
$users = $bc->get_plan()->get_setting('users')->get_value();
$anonymised = $bc->get_plan()->get_setting('anonymize')->get_value();
$filename = backup_plan_dbops::get_default_backup_filename($format, $type, $id, $users, $anonymised);
$bc->get_plan()->get_setting('filename')->set_value($filename);

// Execution.
$bc->finish_ui();
$bc->execute_plan();
$results = $bc->get_results();
$file = $results['backup_destination']; // May be empty if file already moved to target location.

// Do we need to store backup somewhere else?
if (!empty($dir)) {
    if ($file) {
        mtrace("Writing " . $dir.'/'.$filename);
        if ($file->copy_content_to($dir.'/'.$filename)) {
            $file->delete();
            mtrace("Backup completed.");
        } else {
            mtrace("Destination directory does not exist or is not writable. Leaving the backup in the course backup file area.");
        }
    }
} else {
    mtrace("Backup completed, the new file is listed in the backup area of the given course");
}
$bc->destroy();
exit(0);