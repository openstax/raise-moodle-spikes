# Events demos

## Demo lesson for events plugin

The `events-lesson.mbz` file in this directory can be uploaded to a Moodle course. It will create a lesson activity called `Demo lesson` which was used to demonstrate both A/B testing and event generation from Moodle to s3.

## Demo event data generator

To demonstrate analyzing event data, we used the `event_generator.py` script in this directory to generate bulk synthetic event files which can then be uploaded to s3. For example:

```bash
$ python event_generator.py
$ aws s3 cp --recursive .  s3://<s3_bucket>/<s3_prefix>/ --exclude "*" --include "*.json"
$ rm *.json
```

The data can be deleted as needed:

```bash
$ aws s3 rm --recursive s3://<s3_bucket>/<s3_prefix> --include "*.json"
```

# Demo event analyzer

Once an S3 bucket is populated with generated event data, the demo analyzer in this directory can be packaged and run on a k8s cluster:

```bash
$ export REPOHOST=<account>.dkr.ecr.<region>.amazonaws.com
$ export TAG=<tagvalue>
$ aws ecr get-login-password | docker login --username AWS --password-stdin $REPOHOST
$ docker build analyzer/. -t $REPOHOST/moodle-events-analyzer:$TAG
$ docker push $REPOHOST/moodle-events-analyzer:$TAG
$ kubectl run moodle-events-analyzer --image=$REPOHOST/moodle-events-analyzer:$TAG --restart='Never' --env="S3_BUCKET=<s3_bucket>" --env="S3_DATA_PREFIX=<s3_data_prefix>" --env="S3_RESULT_PREFIX=<s3_result_prefix>"
```

Once the pod is running, you can track the logs:

```bash
$ kubectl logs -f moodle-events-analyzer
```

After the job has completed, the pod can be deleted and results can be copied locally:

```bash
$ kubectl delete po moodle-events-analyzer
$ aws s3 cp s3://<s3_bucket>/<s3_result_prefix>/report.csv report.csv
```
