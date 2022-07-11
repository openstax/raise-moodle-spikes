# RAISE Moodle Spikes

This repository contains spike code from Moodle related experimentation for the RAISE project. As such, everything here should be considered as quick and dirty prototypes created to better understand and / or demonstrate potential capabilities.

## Directory structure

The following table describes the directories in this repo:

| Directory | Description |
| - | - |
| `moodle` | Docker files for building development Moodle images that can be deployed locally using `docker-compose` or on Kubernetes using `helm` |
| `deploy` | Deployment automation code |
| `plugins` | Moodle plugins |
| `services` | Ancillary services used to implement / demonstrate functionality |
| `demos` | Miscellaneous code / files used for demos |
| `scripts` | Utility / helper scripts |

## How Tos

### Deploying a local environment

You can use the following commands to get a basic local environment running using `docker-compose` (you may want to modify values in `.env` beforehand):

```bash
$ docker-compose up -d
$ docker-compose exec moodle php admin/cli/install_database.php --agree-license --fullname="Local Dev" --shortname="Local Dev" --summary="Local Dev" --adminpass="admin" --adminemail="admin@acmeinc.com"
```

The site will then be available at [http://localhost:8000/](http://localhost:8000/).

If you want to deploy `kafka` and related services you can include `--profile kafka` to the `docker-compose` invocation (they're not enabled by default to optimize for the current common case):

```bash
$ docker-compose --profile kafka up -d
```

### Debugging in a local environment

You can configure your local development environment to debug Moodle in VScode using the following steps:

1. Install [xdebug](https://xdebug.org/) in your environment
2. Install the [php-debug](https://marketplace.visualstudio.com/items?itemName=felixfbecker.php-debug) extension in VS Code
3. Create a `launch.json` with an appropriate `pathMappings` if you want to set break points in the editor:

```json
{
    "name": "Listen for Xdebug",
    "type": "php",
    "request": "launch",
    "port": 9003,
    "pathMappings": {
        "/var/www/html/admin/tool/events": "${workspaceFolder}/plugins/events"
    }
}
```
4. Setup `moodle` container for debugging:

```bash
$ MOODLE_TARGET=dbg docker-compose build
$ docker-compose up -d
```

#### Moodle settings for debugging

If you are debugging / developing, you may want to modify the following settings within Moodle as well:

* `Site Administration -> Development -> Debugging`: Set "Debug messages" to "Developer"
* `Site Administration -> Appearance -> AJAX and Javascript`: Clear the flag for "Cache Javascript"

### Access mail sent by Moodle

It's sometimes useful to be able to see the emails Moodle is trying to send to users. The environments in this repo configure [MailHog](https://github.com/mailhog/MailHog) so developers can inspect these emails without a real SMTP setup. In a local docker environment, you can navigate to [http://localhost:8025](http://localhost:8025) to see the MailHog web interface. If you have `enableMailhog` enabled for a Kubernetes deployment, the interface can be opened on your development machine by using `kubectl` to port forward:

```bash
$ kubectl port-forward $(kubectl get po -l "app=raise-spikes-mailhog-<deploymentName>" -o name) 8025:8025
```

### Running phpunit tests

Tests can be invoked after setting up `phpunit`:

```bash
$ docker-compose exec moodle php admin/tool/phpunit/cli/init.php
$ docker-compose exec moodle vendor/bin/phpunit --filter <testcase>
```

### Creating a Moodle backup file for git storage

The environment in this repo can be used to create a `.mbz` file for git storage of course backup data from an arbritrary instance. All this script really does is load the content in a clean database and re-export using automated steps for consistency.

**NOTE:** Running this script will delete all of the data in your local Moodle instance.

Example steps:

```bash
$ ./scripts/gitify_mbz.sh -i input.mbz -o output.mbz
```
