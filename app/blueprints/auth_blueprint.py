from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.auth_controller import AuthController

url_prefix = '{}/auth'.format(BaseBlueprint.base_url_prefix)
auth_blueprint = Blueprint('auth', __name__, url_prefix=url_prefix)

auth_controller = AuthController(request)


@auth_blueprint.route('/login', methods=['POST'])
@Security.validator(['email|required', 'password|required'])
def login():
	return auth_controller.login()


@auth_blueprint.route('/admin/login', methods=['POST'])
@Security.validator(['email|required', 'password|required'])
def admin_login():
	return auth_controller.login(admin=True)

