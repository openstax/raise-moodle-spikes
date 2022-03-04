# RAISE Moodle Spikes

This repository contains spike code from Moodle related experimentation for the RAISE project. As such, everything here should be considered as quick and dirty prototypes created to better understand and / or demonstrate potential capabilities.

## Directory structure

The following table describes the directories in this repo:

| Directory | Description |
| - | - |
| `moodle` | Docker files for building development Moodle images that can be deployed locally using `docker-compose` or on Kubernetes using `helm` |
| `chart` | A Helm chart used to deploy systems to k8s clusters |
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

### Deploying to Kubernetes

This repository includes a Helm chart that can be used to easily deploy an instance of Moodle to a Kubernetes cluster. A few notes regarding the implementation of the chart:

* It provisions persistent volumes for the PostgreSQL database and Moodle's data directory. These get mapped to EBS volumes on AWS, and you can adjust the size of these volumes by overriding the default chart values.
* Moodle has a [cron process](https://docs.moodle.org/311/en/Cron) which requires access to both the database and the data directory. The chart implements this by creating a sidecar container in the Moodle deployment pod so the persistent volume can be attached to both containers.
* When using an `https` endpoint (e.g. if you want your Moodle instance to be externally accessible), the chart assumes support for `Certificate` and `IngressRoute` resources via [Cert-manager](https://cert-manager.io/) and Traefik respectively.

#### Pushing images to ECR

Before deploying, you will need to push your dev images to ECR:

```bash
$ export REPOHOST=<account>.dkr.ecr.<region>.amazonaws.com
$ export TAG=<tagvalue>
$ aws ecr get-login-password | docker login --username AWS --password-stdin $REPOHOST
$ docker build . --platform=linux/amd64 -f moodle/Dockerfile -t $REPOHOST/moodle:$TAG
$ docker push $REPOHOST/moodle:$TAG
$ docker build services/eventsapi/. --platform=linux/amd64 -t $REPOHOST/moodle-eventsapi:$TAG
$ docker push $REPOHOST/moodle-eventsapi:$TAG
```

#### Deploying with Helm

You should create a copy of the file `chart/values.yaml` and update the values for your deployment (referred to below as `myvalues.yaml`). You can then deploy with the following steps:

```bash
$ helm upgrade --install -f myvalues.yaml raise-moodle-<deploymentName> chart/
```

**NOTE:** If you set `moodleWebRoot` to be an `https` endpoint, the chart will attempt to provision a certificate for the domain and also provision an `IngressRoute`. For this to work properly, you must preconfigure DNS to map to the cluster endpoint exposed by your Traefik Ingress Controller.

Once the resources are created and the pods look healthy, you can initialize the instance:

```bash
$ kubectl exec $(kubectl get po -l "app=raise-spikes-moodle-<deploymentName>" -o name) -c raise-spikes-moodle-<deploymentName> -- chown -R www-data:www-data /var/www/moodledata
$ kubectl exec $(kubectl get po -l "app=raise-spikes-moodle-<deploymentName>" -o name) -c raise-spikes-moodle-<deploymentName> -- php admin/cli/install_database.php --agree-license --fullname=<sitename> --shortname=<sitename> --summary=<sitesummary> --adminpass=<adminpassword> --adminemail=<adminemail>
```

If `moodleWebRoot` is left as `http://localhost:8888`, you can access the cluster at [http://localhost:8888](http://localhost:8888) on your machine using `kubectl` to port forward:

```bash
$ kube port-forward $(kubectl get po -l "app=raise-spikes-moodle-<deploymentName>" -o name) 8888:80
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
