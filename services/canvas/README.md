# Canvas LMS instance

For certain testing / demonstrations (e.g. LTI integration), we've setup a Canvas instance on an EC2 node using their [quick start Docker steps](https://github.com/instructure/canvas-lms/tree/master/doc/docker).

## Setup steps

### 1. Build Docker images

```bash
$ git clone --depth 1 https://github.com/instructure/canvas-lms
$ cd canvas-lms
$ ./script/docker_dev_setup.sh # Answer 'y' to all prompts
```

### 2. Update `docker-compose.yml` to include Traefik proxy

In order to expose the service for external access, the generated `docker-compose.yml` can be modified to include a `traefik` instance. Traefik can also generate a certificate using Let's Encrypt so you can access Canvas over `https` without having to setup an ELB. The following provides an example patch to the generated compose file, and an example is also included in this directory (**NOTE**: Modify the `Host` rule with the DNS that is mapped to the instance):

```patch
 # See doc/docker/README.md or https://github.com/instructure/canvas-lms/tree/master/doc/docker
 version: '2.3'
 services:
+  traefik:
+    image: traefik:v2.4
+    depends_on:
+      - web
+    command:
+      - "--providers.docker"
+      - "--providers.docker.exposedByDefault=false"
+      - "--entrypoints.web.address=:80"
+      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
+      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
+      - "--entrypoints.websecure.address=:443"
+      - "--certificatesresolvers.myresolver.acme.httpchallenge=true"
+      - "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web"
+      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
+    volumes:
+      - /var/run/docker.sock:/var/run/docker.sock
+      - letsencrypt:/letsencrypt
+    ports:
+      - 80:80
+      - 443:443
+
   web: &WEB
     build:
       context: .
@@ -9,9 +30,21 @@ services:
       - redis
     environment:
       POSTGRES_PASSWORD: sekret
+      ADDITIONAL_ALLOWED_HOSTS: REPLACE_ME_WITH_HOST_DNS
+    labels:
+      - "traefik.enable=true"
+      - "traefik.http.routers.web.entrypoints=websecure"
+      - "traefik.http.routers.web.rule=Host(`REPLACE_ME_WITH_HOST_DNS`)"
+      - "traefik.http.routers.web.tls.certresolver=myresolver"

   jobs:
-    <<: *WEB
+    build:
+      context: .
+    links:
+      - postgres
+      - redis
+    environment:
+      POSTGRES_PASSWORD: sekret
     command: bundle exec script/delayed_job run

   postgres:
@@ -21,3 +54,5 @@ services:

   redis:
     image: redis:alpine
+volumes:
+  letsencrypt:
```

### 3. Start modified services

```bash
$ docker-compose up -d
```
