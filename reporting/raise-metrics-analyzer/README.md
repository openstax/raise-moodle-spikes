# RAISE Metrics Analyzer

This is a simple script used to build a container image which can be used to analyze RAISE data for product metrics within our AWS environment.

Changes to this code can be pushed to ECR as follows:

```bash
$ export REPOHOST=<account>.dkr.ecr.<region>.amazonaws.com
$ export TAG=latest
$ aws ecr get-login-password | docker login --username AWS --password-stdin $REPOHOST
$ docker build . --platform=linux/amd64 -t $REPOHOST/raise-metrics-analyzer:$TAG
$ docker push $REPOHOST/raise-metrics-analyzer:$TAG
```
