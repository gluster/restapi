# -*- coding: utf-8 -*-
#
#  Copyright (c) 2016 Red Hat, Inc. <http://www.redhat.com>
#  This file is part of GlusterFS.
#
#  This file is licensed to you under your choice of the GNU Lesser
#  General Public License, version 3 or any later version (LGPLv3 or
#  later), or the GNU General Public License, version 2 (GPLv2), in all
#  cases as published by the Free Software Foundation.
#
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from flask import Flask, redirect
from gluster.cli import set_gluster_path

from api_volume import volume_api
from api_peer import peer_api
from api_georep import georep_api
from utils import http_response_error
from conf import VERSION

app = Flask(__name__)


app.register_blueprint(volume_api, url_prefix=VERSION + "/volumes")
app.register_blueprint(peer_api, url_prefix=VERSION + "/peers")
app.register_blueprint(georep_api, url_prefix=VERSION + "/georep")


@app.errorhandler(404)
def page_not_found(e):
    return http_response_error("Not Found", status=404)


@app.route("/doc")
def doc():
    return ""


@app.route("/")
def home():
    return redirect(VERSION + "/doc", code=302)


def main():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=__doc__)
    parser.add_argument("--port", type=int, help="Port", default=9000)
    parser.add_argument("--debug", help="Run Server in debug mode",
                        action="store_true")
    parser.add_argument("--gluster-path", help="Path of gluster Command")
    args = parser.parse_args()

    if args.gluster_path:
        set_gluster_path(args.gluster_path)

    if args.debug:
        app.debug = True

    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
