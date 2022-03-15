# Content plugin

This plugin is a proof-of-concept for using / storing HTML content outside of Moodle. Specifically it validates that a content developer can use a simple short code such as the following in Moodle:

```
[osx-raise id="content-id"]
```

The plugin will then try to fetch / insert this content from the browser. If you want to force the plugin to render in the backend, you can set the `FILTER_CONTENT_BE` in the moodle container in `docker-compose.yml`:

```yaml
    environment: &moodleenv
      FILTER_CONTENT_BE: "1"
```
