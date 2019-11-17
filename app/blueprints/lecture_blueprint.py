from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth

url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
lecture_blueprint = Blueprint('lecture', __name__, url_prefix=url_prefix)
	