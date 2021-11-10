<?php

defined('MOODLE_INTERNAL') || die;

function generate_ssotoken($research_id, $key) {
    // Generate token timestamp and expiration as ISO8601 strings
    $current_time = new DateTime('now');
    $timestamp = $current_time->format('c');
    // Expire token after 1 hour
    $expiration = $current_time->add(new DateInterval('PT1H'))->format('c');

    // NOTE: It doesn't seem like Qualtrics respects the expiration, but
    // including that and timestamp anyways.
    $query_data = array(
        'timestamp' => $timestamp,
        'expiration' => $expiration,
        'research_id' => $research_id
    );

    // Explicitly passing arg separator to http_build_query to account for
    // the following as otherwise we'll end up with an incorrect hash: https://github.com/moodle/moodle/blob/5ea35451152140314ad8b2da6118700c6f8a43f3/lib/setup.php#L746-L747
    $raw_query = http_build_query($query_data, "", "&");

    $hash = base64_encode(
        hash_hmac('md5', $raw_query, $key, true)
    );
    $token = $raw_query.'&mac='.$hash;

    $encryptedtoken =  openssl_encrypt(
        $token,
        'aes-128-ecb',
        $key
    );

    // Return a URL encoded token
    return urlencode($encryptedtoken);
}

function get_or_create_research_id() {
    global $USER, $DB;

    $research_id = $DB->get_record(
        'study_research_identifier',
        array('user_id'=>$USER->id),
        '*',
        IGNORE_MISSING
    );

    if ($research_id) {
        $uuid = $research_id->research_uuid;
    } else {
        // Create a new identifier for this user
        $uuid = \core\uuid::generate();
        $research_identifier = new stdClass();
        $research_identifier->user_id = $USER->id;
        $research_identifier->research_uuid = $uuid;
        $DB->insert_record('study_research_identifier', $research_identifier);
    }

    return $uuid;
}
