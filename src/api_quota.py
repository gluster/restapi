# volume quota <VOLNAME> {enable|disable|list [<path> ...]| list-objects [<path> ...] | remove <path>| remove-objects <path> | default-soft-limit <percent>} |
# volume quota <VOLNAME> {limit-usage <path> <size> [<percent>]} |
# volume quota <VOLNAME> {limit-objects <path> <number> [<percent>]} |
# volume quota <VOLNAME> {alert-time|soft-timeout|hard-timeout} {<time>} - quota translator specific operations
# volume inode-quota <VOLNAME> enable - quota translator specific operations
from utils import auth, gluster_cmd_to_http_response
from gluster.cli import volume
from flask import Blueprint

quota_api = Blueprint('quota_api', __name__)


@quota_api.route("/<name>/inode-quota", methods=["POST"])
@auth
def api_volume_inode_quota_enable(name):
    return gluster_cmd_to_http_response(volume.quota.inode_quota_enable, name)


@quota_api.route("/<name>/quota", methods=["POST"])
@auth
def api_volume_quota_enable(name):
    return gluster_cmd_to_http_response(volume.quota.enable, name)


@quota_api.route("/<name>/quota", methods=["DELETE"])
@auth
def api_volume_quota_disable(name):
    return gluster_cmd_to_http_response(volume.quota.disable, name)


@quota_api.route("/<name>/quota/limit-usage", methods=["POST"])
@auth
def api_volume_inode_quota_limit_usage(name):
    return gluster_cmd_to_http_response(volume.quota.inode_quota_enable, name)
