from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
event_blueprint = Blueprint('event', __name__, url_prefix=url_prefix)
	