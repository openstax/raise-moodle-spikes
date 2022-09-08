# Demo enclave orchestration

This directory contains example files of how we might employ [Argo](https://argoproj.github.io/) and k8s [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) to operationalize enclaves on a Kubernetes cluster. Specifically:

* `workflow.yaml` - This is an example of a file that can be executed as `argo submit workflow.yaml` and implements a simple chained workflow with three stages. The sample can be modified with desired container `image` and `command` values for each stage for testing / experimentation.

* `networkpolicy.yaml` - This is a configuration that defines a policy imposed on any cluster pod with `role=enclave` to disallow ingress and egress network access. It ties to the metadata associated with the `analyze` step in `workflow.yaml`. This is arbritrary for the example, and we may decide on a different selector in practice later.
