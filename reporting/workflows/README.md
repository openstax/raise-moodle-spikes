# RAISE data workflow

The files in this directory include `argo` and `k8s` configuration files used to deploy a daily periodic job which:

1. Pushes data from Moodle to s3
2. Runs the `raise-data-analyzer` code and pushes results to s3

The `raise-data-moodle-creds.yaml` file can be used as a template to rotate the token that allows this automated job to talk to Moodle. Simply change `sometokenvalue` to the desired value:

```bash
$ kubectl apply -f raise-data-moodle-creds.yaml
```

The argo job was created using the CLI:

```bash
$ argo cron create raise-data-daily.yaml
```
