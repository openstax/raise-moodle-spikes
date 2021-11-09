# RAISE Moodle Spikes

This repository contains spike code from Moodle related experimentation for the RAISE project. As such, everything here should be considered as quick and dirty prototypes created to better understand and / or demonstrate potential capabilities.

## Directory structure

The following table describes the directories in this repo:

| Directory | Description |
| - | - |
| `moodle` | Docker files for building development Moodle images that can be deployed locally using `docker-compose` or on Kubernetes using `helm` |
| `chart` | A Helm chart used to deploy systems to k8s clusters |

## How Tos

### Deploying a local environment

You can use the following commands to get a basic local environment running using `docker-compose` (you may want to modify values in `.env` beforehand):

```bash
$ docker-compose up -d
$ docker-compose exec moodle php admin/cli/install_database.php --agree-license --fullname="Dev site" --shortname="dev_site" --summary="Dev moodle site" --adminpass="admin" --adminemail="admin@acmeinc.com"
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
$ docker build . -f moodle/Dockerfile -t $REPOHOST/moodle:$TAG
$ docker push $REPOHOST/moodle:$TAG
$ docker build services/eventsapi/. -t $REPOHOST/moodle-eventsapi:$TAG
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
