from utils import auth
from flask import Blueprint

georep_api = Blueprint('georep_api', __name__)


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>",
                  methods=["PUT"])
@auth
def api_georep_create(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/start",
                  methods=["POST"])
@auth
def api_georep_start(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/stop",
                  methods=["POST"])
@auth
def api_georep_stop(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>",
                  methods=["DELETE"])
@auth
def api_georep_delete(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/config",
                  methods=["GET"])
@auth
def api_georep_config_get(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/config",
                  methods=["POST"])
@auth
def api_georep_config_set(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/config",
                  methods=["DELETE"])
@auth
def api_georep_config_reset(mastervol, slaveuser, slavehost, slavevol):
    pass


# Multiple routes will go to same function, Status can be fetched with or
# without Volume names
@georep_api.route("", methods=["GET"])
@georep_api.route("/<mastervol>", methods=["GET"])
@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>",
                  methods=["GET"])
@auth
def api_georep_status(mastervol=None, slaveuser=None, slavehost=None,
                      slavevol=None):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/checkpoint",
                  methods=["POST"])
@auth
def api_checkpoint_set(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/checkpoint",
                  methods=["GET"])
@auth
def api_checkpoint_get(mastervol, slaveuser, slavehost, slavevol):
    pass


@georep_api.route("/<mastervol>/<slaveuser>/<slavehost>/<slavevol>/checkpoint",
                  methods=["DELETE"])
@auth
def api_checkpoint_del(mastervol, slaveuser, slavehost, slavevol):
    pass


# Pause
# Resume
