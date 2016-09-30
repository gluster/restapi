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

from utils import auth, gluster_cmd_to_http_response, boolify
from gluster.cli import volume
from flask import Blueprint, request

volume_api = Blueprint('volume_api', __name__)


def validate_volume_create_options(data):
    # def create(volname, bricks, replica=0, stripe=0, arbiter=0, disperse=0,
    #        disperse_data=0, redundancy=0, transport="tcp", force=False):
    # for k in data.keys():
    #     if k not in ["bricks", "replica", "stripe",
    #                  "arbiter", "disperse", "disperse_data",
    #                  "redundancy", "transport", "force"]:

    pass


@volume_api.route("/<name>", methods=["PUT"])
@auth
def api_volume_create(name):
    data = request.get_json()
    validate_volume_create_options(data)
    bricks = data.get("bricks")
    del data["bricks"]
    return gluster_cmd_to_http_response(volume.create, name, bricks, **data)


@volume_api.route("/<name>/start", methods=["POST"])
@auth
def api_volume_start(name):
    force = boolify(request.form.get("force", "0"))
    return gluster_cmd_to_http_response(volume.start, name, force=force)


@volume_api.route("/<name>/stop", methods=["POST"])
@auth
def api_volume_stop(name):
    force = boolify(request.form.get("force", "0"))
    return gluster_cmd_to_http_response(volume.stop, name, force=force)


@volume_api.route("/<name>", methods=["DELETE"])
@auth
def api_volume_delete(name):
    force = boolify(request.form.get("force", "0"))
    return gluster_cmd_to_http_response(volume.stop, name, force=force)


@volume_api.route("/<name>", methods=["GET"])
@volume_api.route("", methods=["GET"])
@auth
def api_volume_get(name=None):
    status = boolify(request.args.get("status", "0"))
    if status:
        return gluster_cmd_to_http_response(volume.status_detail, name)
    else:
        return gluster_cmd_to_http_response(volume.info, name)


@volume_api.route("/<name>/options", methods=["GET"])
@auth
def api_volume_options_get(name):
    opt = boolify(request.args.get("option", "all"))
    return gluster_cmd_to_http_response(volume.optget, name, opt)


@volume_api.route("/<name>/options", methods=["POST"])
@auth
def api_volume_options_set(name):
    opts = request.get_json()
    return gluster_cmd_to_http_response(volume.optset, name, opts)


@volume_api.route("/<name>/options", methods=["DELETE"])
@auth
def api_volume_options_reset(name):
    data = request.get_json()
    return gluster_cmd_to_http_response(volume.optreset, name,
                                        data["option"], data["force"])


@volume_api.route("/<name>/rebalance/start", methods=["POST"])
@auth
def api_volume_rebalance_start(name):
    data = request.get_json()
    if data.get("fixed-layout", False):
        return gluster_cmd_to_http_response(volume.rebalance.fix_layout_start,
                                            name)
    else:
        return gluster_cmd_to_http_response(volume.rebalance.start,
                                            name,
                                            force=data.get("force", False))


@volume_api.route("/<name>/rebalance/stop", methods=["POST"])
@auth
def api_volume_rebalance_stop(name):
    return gluster_cmd_to_http_response(volume.rebalance.stop, name)


@volume_api.route("/<name>/rebalance", methods=["GET"])
@auth
def api_volume_rebalance_status(name):
    return gluster_cmd_to_http_response(volume.rebalance.status, name)


@volume_api.route("/<name>/barrier", methods=["POST"])
@auth
def api_volume_barrier_enable(name):
    return gluster_cmd_to_http_response(volume.barrier_enable, name)


@volume_api.route("/<name>/barrier", methods=["DELETE"])
@auth
def api_volume_barrier_disable(name):
    return gluster_cmd_to_http_response(volume.barrier_disable, name)
