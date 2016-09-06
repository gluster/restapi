# Management REST API Server for Gluster

This project is aimed to provide RESTful interface for Gluster
Management activities like Volume Create, Start, Stop
etc by exposing Gluster CLI commands via REST.

REST services will be run in all nodes of Cluster, applications can
send HTTP call to any node of Cluster. Applications can
communicate easily with Gluster Cluster using REST API instead of
running Gluster commands via `ssh` or having agents in each node.

Note: Native REST interface will be available with Glusterd 2.0.

## Installation

This project depends on glustercli-python, Install using

    pip install glustercli

Clone the repo and install using,

    ./autogen.sh
    ./configure
    make install

Usage
-----
Enable and Start glusterrestd service in all Gluster nodes using,

    systemctl enable glusterrestd
    systemctl start glusterrestd

Status can be checked using `gluster-restapi status`.

Register your application using,

    gluster-restapi app-add <APP_ID> <SECRET>

Application should sign all requests using this key, read more
about the signing process in "Authentication" section. This app secret
can be reset any time using

    gluster-restapi app-reset <APP_ID> <SECRET>

Application can be deleted using below command,

    gluster rest app-del <APP_ID>

### Authentication
For POST and PUT requests, the request body must be JSON, with the
`Content-Type` header set to `application/json`

Authorization header must be included with every request. Auth header
should have following details

    Bearer <TOKEN>

Example,

    Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. \
        eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImdsdXN0ZXIiLCJhZG1 \
        pbiI6dHJ1ZX0.5jCURTbAZV0i5f_ux7PYFUzF-waCtYMM0LrF1Zl2hd0"

TOKEN is [JSON Web Token](http://jwt.io/) generated using following claims

    iss: Issuer(Application ID)
    iat: Issued Time
    exp: Expiry time
    qsh: SHA256 hash of resource identifier(Ex: SHA256("GET\n/v1/volumes")

qsh is custom claim used to protect against URL tampering. JWT
signature provides protection against man-in-the-middle modification
of claims, but the same token can be used of multiple URIs. qsh is
SHA256 hash calculated using HTTP Method, URI, Query params and
POST/PUT/DELETE data. qsh claim usage here is similar to
[Heketi](https://github.com/heketi/heketi) and
[Atlassian](https://developer.atlassian.com/blog/2015/01/understanding-jwt/)
projects.

For example, to calculate qsh for `GET /v1/volumes?status=1`

    string_to_hash = "GET\n/v1/volumes\nstatus=1"
    qsh = sha256(string_to_hash)

To calculate qsh for `POST /v1/volumes/gv1/start -d '{"force": true}'`

    post_data = '{"force": true}'
    string_to_hash = "POST\n/v1/volumes/gv1/start\n${post_data}"
    qsh = sha256(string_to_hash)

Following example shows generation of JWT and making REST call(using Python)

    import hashlib
    from datetime import datetime, timedelta

    import jwt
    import requests

    APP_ID = "myapp"
    APP_SECRET = "myappsecret"
    BASE_URL = "http://localhost:8080"
    URL = "/v1/volumes"

    qsh_data = "GET\n" + URL
    qsh = hashlib.sha256(qsh_data).hexdigest()
    claims = {
        "iss": APP_ID,
        "qsh": qsh,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(claims, APP_SECRET, algorithm='HS256')
    headers = {
        "Authorization": "Bearer {0}".format(token)
    }

    volinfo = requests.get(BASE_URL + URL, headers=headers)

### Consuming REST APIs
Applications can persist the peers list(`GET /v1/peers`) of the
Cluster. Application can connect to any node of Cluster and consume
REST APIs, if a connected node goes down in Cluster, application can
choose another node to make REST calls.

### Configuration

REST server can be configured using `config` subcommand.

    gluster-restapi config-get [<NAME>]
    gluster-restapi config-set <NAME> <VALUE>
    gluster-restapi config-reset <NAME|all>

Available configurations,

    https enabled    # Enable https
    port  443        # Port of REST Service
    auth  enabled    # Enable Authentication

## API Documentation
-----------------
Coming Soon


## Comments and Discussion
[JWT Shared secret vs Shared Token](http://www.gluster.org/pipermail/gluster-devel/2016-March/048508.html)
