from utils import auth
from flask import Blueprint

peer_api = Blueprint('peer_api', __name__)


@peer_api.route("/<fqdn>", methods=["PUT"])
@auth
def api_peer_attach(fqdn):
    pass


@peer_api.route("/<fqdn>", methods=["DELETE"])
@auth
def api_peer_detach(fqdn):
    pass


@peer_api.route("", methods=["GET"])
@auth
def api_peer_info():
    pass
