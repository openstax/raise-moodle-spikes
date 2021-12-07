<?php

namespace core\oauth2\service;

use core\oauth2\issuer;
use core\oauth2\discovery\openidconnect;
use core\oauth2\endpoint;
use core\oauth2\user_field_mapping;

class clever extends openidconnect implements issuer_interface {
    /**
     * Build an OAuth2 issuer, with all the default values for this service.
     *
     * @return issuer The issuer initialised with proper default values.
     */
    public static function init(): issuer {
        $record = (object) [
            'name' => 'Clever',
            'image' => 'https://apps.clever.com/favicon.ico',
            'basicauth' => 1,
            'baseurl' => '',
            'showonloginpage' => issuer::LOGINONLY,
            'servicetype' => 'clever',
        ];

        $issuer = new issuer(0, $record);
        return $issuer;
    }

    /**
     * Create endpoints for this issuer.
     *
     * @param issuer $issuer Issuer the endpoints should be created for.
     * @return issuer
     */
    public static function create_endpoints(issuer $issuer): issuer {
        $endpoints = [
            'authorization_endpoint' => 'https://clever.com/oauth/authorize',
            'token_endpoint' => 'https://clever.com/oauth/tokens',
            'userinfo_endpoint' => 'https://api.clever.com/v3.0/me',
            'userdata_endpoint' => 'https://api.clever.com/v3.0/users'
        ];
        foreach ($endpoints as $name => $url) {
            $record = (object) [
                'issuerid' => $issuer->get('id'),
                'name' => $name,
                'url' => $url
            ];
            $endpoint = new endpoint(0, $record);
            $endpoint->create();
        }

        // Create the field mappings.
        $mapping = [
            'data-id' => 'idnumber',
            'data-name-first' => 'firstname',
            'data-name-last' => 'lastname',
            'data-email' => 'email'
        ];
        foreach ($mapping as $external => $internal) {
            $record = (object) [
                'issuerid' => $issuer->get('id'),
                'externalfield' => $external,
                'internalfield' => $internal
            ];
            $userfieldmapping = new user_field_mapping(0, $record);
            $userfieldmapping->create();
        }

        return $issuer;
    }
}
