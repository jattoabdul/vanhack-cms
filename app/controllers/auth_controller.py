from datetime import timedelta

from app.controllers.base_controller import BaseController
from app.controllers.account_controller import AccountController
from app.repositories.student_repo import StudentRepo
from app.repositories.admin_repo import AdminRepo
from app.utils.security import Security
from flask_jwt_extended import create_access_token


class AuthController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.student_repo = StudentRepo()
		self.admin_repo = AdminRepo()
	
	def login(self, admin=False):
		
		email, password = self.request_params('email', 'password')

		if admin:
			user = self.admin_repo.find_first(email=email, is_deleted=False)
		else:
			user = self.student_repo.find_first(email=email, is_deleted=False)
		
		if user and user.is_deleted is False:
			if Security.is_password_valid(password, user.password):

				user_object = {**user.serialize(excluded=['password']), **{'authKey': user.auth_key}}
				expires = timedelta(days=30)
				access_token = create_access_token(identity=user_object, expires_delta=expires)
				return self.handle_response('OK', payload={'token': access_token})
			
			return self.handle_response('Invalid Email or Password Supplied', status_code=400)
		
		return self.handle_response('No User Account Found', status_code=400)
