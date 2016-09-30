## Installation

This project depends on `glustercli-python`. Install `glustercli-python` using,

    git clone https://github.com/gluster/glustercli-python.git
    cd glustercli-python
    python setup.py install

Install Gluster REST APIs using,

    git clone https://github.com/gluster/restapi.git
    cd restapi
    ./autogen.sh
    ./configure --with-systemddir=/usr/lib/systemd/system/ \
        --with-glusterd-workdir=/var/lib/glusterd \
        --with-gluster-libexecdir=/usr/libexec/glusterfs
    make
    make install
    
For systems which are not using systemd can pass
`--with-initdir=/etc/init.d` or `--with-initdir=/etc/rc.d` to install
service files.

## Setup

Gluster REST Servers can be run in one or more nodes of Cluster
depending on the High availability requirement.

Enable and Start `glusterrest` service in all required peer nodes.

(Systemd)

    systemctl enable glusterrestd
    systemctl start glusterrestd

(SysVInit - CentOS 6)

    chkconfig glusterrestd on
    service glusterrestd start

(FreeBSD) Add the following in `/etc/rc.conf`

glusterrestd_enable="YES"

And start the glusterrestd using,

    service glusterrestd start

## Status

Status Can be checked using,

    gluster-eventsapi status

Example output:

    +-----------+-------------+-----------------------+
    |    NODE   | NODE STATUS | GLUSTERRESTD STATUS   |
    +-----------+-------------+-----------------------+
    | localhost |          UP |                    UP |
    | node2     |          UP |                    UP |
    +-----------+-------------+-----------------------+

## Configuration

View all configurations using,

    usage: gluster-restapi config-get [-h] [--name NAME]
     
    optional arguments:
      -h, --help   show this help message and exit
      --name NAME  Config Name

Example output:

    +--------------+-----------------------------+
    |         NAME | VALUE                       |
    +--------------+-----------------------------+
    |        https | False                       |
    |  num-workers | 2                           |
    |          key | /etc/glusterrest/server.key |
    | auth-enabled | True                        |
    |         port | 8080                        |
    |          csr | /etc/glusterrest/server.csr |
    +--------------+-----------------------------+

To change any configuration,

    usage: gluster-restapi config-set [-h] name value
     
    positional arguments:
      name        Config Name
      value       Config Value
     
    optional arguments:
      -h, --help  show this help message and exit

Example output,

    +-----------+-------------+-------------+
    |    NODE   | NODE STATUS | SYNC STATUS |
    +-----------+-------------+-------------+
    | localhost |          UP |          OK |
    | node2     |          UP |          OK |
    +-----------+-------------+-------------+

To Reset any configuration,

    usage: gluster-restapi config-reset [-h] name
     
    positional arguments:
      name        Config Name or all
     
    optional arguments:
      -h, --help  show this help message and exit

Example output,

    +-----------+-------------+-------------+
    |    NODE   | NODE STATUS | SYNC STATUS |
    +-----------+-------------+-------------+
    | localhost |          UP |          OK |
    | node2     |          UP |          OK |
    +-----------+-------------+-------------+

**Note**: If any node status is not UP or sync status is not OK, make
  sure to run `gluster-restapi sync` from a peer node.

## Add node to the Cluster

When a new node added to the cluster,

- Enable and Start `glusterrestd` in the new node using the steps
  mentioned above
- Run `gluster-restapi sync` command from a peer node other than the
  new node.

## Applications

If Auth is enabled using, `gluster-restapi config-set auth-enabled
true` then Application needs to be registered using `gluster-restapi
app-add` command.

JSON Web Tokens are used for authenticating REST calls.

Add Application,

    usage: gluster-restapi app-add [-h] appid appsecret
     
    positional arguments:
      appid       Application ID
      appsecret   Application Secret
     
    optional arguments:
      -h, --help  show this help message and exit

Reset Application Secret,

    usage: gluster-restapi app-reset [-h] appid appsecret
     
    positional arguments:
      appid       Application ID
      appsecret   Application Secret
     
    optional arguments:
      -h, --help  show this help message and exit

Delete Application using,

    usage: gluster-restapi app-del [-h] appid
     
    positional arguments:
      appid       Application ID
     
    optional arguments:
      -h, --help  show this help message and exit


Example,

    gluster-restapi app-add mywebapp mywebappsecret

## Authentication

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
[Atlassian](https://developer.atlassian.com/blog/2015/01/understanding-jwt/)
project.

For example, to calculate qsh for `GET /v1/volumes?status=1`

    string_to_hash = "GET\n/v1/volumes\nstatus=1"
    qsh = sha256(string_to_hash)

To calculate qsh for `POST /v1/volumes/gv1/start -d '{"force": true}'`

    post_data = '{"force": true}'  # Sort By Keys
    string_to_hash = "POST\n/v1/volumes/gv1/start\n${post_data}"
    qsh = sha256(string_to_hash)

Following example shows generation of JWT and making REST call(using Python)

    import hashlib
    from datetime import datetime, timedelta

    import jwt
    import requests

    APP_ID = "mywebapp"
    APP_SECRET = "mywebappsecret"
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

## REST Client

TODO
