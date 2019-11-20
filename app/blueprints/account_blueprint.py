from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.account_controller import AccountController

url_prefix = '{}/accounts'.format(BaseBlueprint.base_url_prefix)
account_blueprint = Blueprint('account', __name__, url_prefix=url_prefix)

account_controller = AccountController(request)

""" Student BluePrints """


@account_blueprint.route('/student/signup', methods=['POST'])
@Security.validator([
    'first_name|required', 'last_name|required',
    'email|not-exist|student|email', 'email|required',
    'password|required']
)
def student_register():
    return account_controller.register(admin=False)


@account_blueprint.route('/student/<int:id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('student')
def update_student_account(id):
    return account_controller.update_student_account(id, admin=False)


@account_blueprint.route('/student/me', methods=['GET'])
@Auth.has_permission('student')
def me():
    return account_controller.fetch_student_account(id=0, admin=False)


@account_blueprint.route('/student/me/verify', methods=['PUT', 'PATCH'])
@Auth.has_permission('student')
def verify_student_account():
    return account_controller.verify_student(id=0, admin=False)


@account_blueprint.route('/student/premium/confirm', methods=['PUT', 'PATCH'])
@Auth.has_permission('student')
def student_confirm_premium_account():
    return account_controller.toggle_premium_student(id=0, admin=False, confirm=True)


@account_blueprint.route('/student/premium/unconfirm', methods=['PUT', 'PATCH'])
@Auth.has_permission('student')
def student_unconfirm_premium_account():
    return account_controller.toggle_premium_student(id=0, admin=False, confirm=False)


""" Admin BluePrints """


@account_blueprint.route('/admin/me', methods=['GET'])
@Auth.has_permission('admin')
def admin_me():
    return account_controller.fetch_my_admin_account()


@account_blueprint.route('/students', methods=['GET'])
@Auth.has_permission('admin')
def list_student_accounts():
    return account_controller.fetch_list(account_type='student')


@account_blueprint.route('/admin/signup', methods=['POST'])
@Security.validator([
    'first_name|required', 'last_name|required',
    'email|not-exist|admin|email', 'email|required',
    'password|required']
)
def admin_register():
    return account_controller.register(admin=True)


@account_blueprint.route('/admin/student/<int:id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def admin_update_student_account(id):
    return account_controller.update_student_account(id, admin=True)


@account_blueprint.route('/admin/student/<int:student_id>', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_student_account(student_id):
    return account_controller.fetch_student_account(student_id, admin=True)


@account_blueprint.route('/admin/<int:id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def update_admin_account(id):
    return account_controller.update_staff_account(id)


@account_blueprint.route('/admin/<int:admin_id>', methods=['GET'])
@Auth.has_permission('admin')
def fetch_single_admin_account(admin_id):
    return account_controller.fetch_admin_account(admin_id)


@account_blueprint.route('/admin/student/<int:id>/verify', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def admin_verify_student_account(id):
    return account_controller.verify_student(id, admin=True)


@account_blueprint.route('/admin/student/<int:id>/premium/confirm', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def admin_confirm_premium_account(id):
    return account_controller.toggle_premium_student(id, admin=True, confirm=True)


@account_blueprint.route('/admin/student/<int:id>/premium/unconfirm', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def admin_unconfirm_premium_account(id):
    return account_controller.toggle_premium_student(id, admin=True, confirm=False)


@account_blueprint.route('/admins', methods=['GET'])
@Auth.has_permission('admin')
def list_admin_accounts():
    return account_controller.fetch_list(account_type='admin')
