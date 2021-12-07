<?php

namespace core\oauth2\client;

use core\oauth2\client;

class clever extends client {
    /**
     * Fetch the user id from the userinfo endpoint and then query userdata
     *
     * @return array|false
     */
    public function get_userinfo() {
        $userinfo = parent::get_userinfo();
        $userid = $userinfo['idnumber'];

        return $this->get_userdata($userid);
    }

    /**
     * Obtain user name and email data via the userdata endpoint
     *
     * @param string $userid User ID value
     * @return array|false
     */
    private function get_userdata($userid) {
        $url = $this->get_issuer()->get_endpoint_url('userdata');
        $url .= '/' . $userid;

        $response = $this->get($url);
        if (!$response) {
            return false;
        }
        $userinfo = new \stdClass();
        try {
            $userinfo = json_decode($response);
        } catch (\Exception $e) {
            return false;
        }

        return $this->map_userinfo_to_fields($userinfo);
    }
}
