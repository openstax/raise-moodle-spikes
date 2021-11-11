<?php

defined('MOODLE_INTERNAL') || die;

require_once ($CFG->dirroot.'/course/moodleform_mod.php');

class mod_study_mod_form extends moodleform_mod {
    function definition() {
        $mform = $this->_form;

        $mform->addElement('header', 'general', get_string('general', 'form'));

        $mform->addElement('text', 'name', get_string('name'), array('size'=>'48'));
        $mform->addRule('name', null, 'required', null, 'client');
        $mform->addRule('name', get_string('maximumchars', '', 255), 'maxlength', 255, 'client');
        $mform->setType('name', PARAM_TEXT);

        $mform->addElement('url', 'studyurl', get_string('studyurl', 'study'), array('size'=>'60'), array('usefilepicker'=>false));
        $mform->addRule('studyurl', null, 'required', null, 'client');
        $mform->addRule('studyurl', get_string('maximumchars', '', 255), 'maxlength', 255, 'client');
        $mform->setType('studyurl', PARAM_RAW_TRIMMED);

        $mform->addElement('text', 'secretkey', get_string('secretkey', 'study'), array('size'=>'60'));
        $mform->addRule('secretkey', null, 'required', null, 'client');
        $mform->addRule('secretkey', get_string('maximumchars', '', 255), 'maxlength', 255, 'client');
        $mform->setType('secretkey', PARAM_TEXT);

        $this->standard_intro_elements();
        $this->standard_coursemodule_elements();
        $this->add_action_buttons();
    }
}
