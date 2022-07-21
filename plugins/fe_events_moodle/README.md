# Local FE Events moodle Webservice Plugin 

This plugin exposes an webservice enpoint (AJAX capable) that receives events and dispatches moodle events to the events
plugin event observer.

## Testing with Raise-MoodleCLI

The simplest way to test this plugin is to open up the raise-moodlecli tool that can be found at https://github.com/openstax/raise-moodlecli. This CLI contains a command - 'log-event-manually moodle' which will exercise the AJAX endpoint with a phoney event. 

The CLI needs two env variables set before it can find your moodle instance MOODLE_URL - the url of your moodle instance, and MOODLE_TOKEN - a valid token for using the endpoint. (see below)

Once configured, you should be able to see requests being forwarded to the events api by running:
```bash
$ docker-compose logs -f eventsapi
```

### Generating a Token for the Endpoint

1. While logged in as a sys admin, navigate to Site Administration / Server / External Services 
2. If you see the relevant external service already, skip to step 4, otherwisse click 'Add' in the bottom left, name your External Service, check 'Enable', and save
3. Navigate back to Server / External services, click on 'functions' under the service you just created, then add 'local_fe_events_moodle_content_loaded_handler' as a function and save

4. Navigate to Sys Admin / Server / Manage Tokens. If you see a relevant token already copy it to your . Otherwise click 'Create Token'
5. Under 'User' add the sys admin, and under 'Service' add the relevant External Service Name then save
6. Copy the newly generated token
