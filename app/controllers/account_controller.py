from datetime import timedelta
import json
from app.controllers.base_controller import BaseController
from app.repositories.student_repo import StudentRepo
from app.repositories.admin_repo import AdminRepo
from app.utils.security import Security
from flask_jwt_extended import create_access_token
from flask import render_template, redirect
import hashlib
from config import get_env


# from app.utils import random_number


class AccountController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.student_repo = StudentRepo()
		self.admin_repo = AdminRepo()

	def register(self, admin=False):
		first_name, last_name, email, password, is_lecturer, is_verified, is_premium = self.request_params(
			'first_name', 'last_name', 'email', 'password', 'is_lecturer',
			'is_verified', 'is_premium'
		)

		try:
			password_hash = Security.hash_password(password)
		except Exception as e:
			print(e)
			return self.handle_response('Application Error - err: 9000', status_code=500)

		if admin:
			user = self.admin_repo.new_user(
				first_name=first_name, last_name=last_name, email=email, password=password_hash,
				is_lecturer=is_lecturer
			)

			if user:
				user = AdminRepo.refresh_auth_key(user)
				token = create_access_token(
					identity={**user.serialize(), **{'authKey': user.auth_key}})
		else:
			user = self.student_repo.new_user(
				first_name=first_name, last_name=last_name, email=email, password=password_hash,
				is_verified=is_verified, is_premium=is_premium
			)

			if user:
				user = StudentRepo.refresh_auth_key(user)
				token = create_access_token(
					identity={**user.serialize(), **{'authKey': user.auth_key}})

		if user and token:
			return self.handle_response('OK', payload={'token': token})

		return self.handle_response('Server Failed To Handle Request. Please Retry Later', status_code=503)

	def update_student_account(self, id, admin=False):
		student_id = self.user('id')
		if admin:
			student_id = id

		student = self.student_repo.find_first(id=student_id, is_deleted=False)

		first_name, last_name, email = self.request_params('first_name', 'last_name', 'email')

		if student:
			updates = {}

			if first_name:
				updates['first_name'] = first_name

			if last_name:
				updates['last_name'] = last_name

			if email and student.email != email:
				if self.student_repo.find_first(email=email):
					return self.handle_response('Email Already In Use', status_code=400)
				updates['email'] = email

			if len(updates) == 0:
				return self.handle_response('No Changes Made - No Parameters To Update', status_code=403)

			student = self.student_repo.update(student, **updates)
			student_object = {**student.serialize(excluded=['password'])}
			expires = timedelta(days=30)
			refresh_token = create_access_token(identity=student_object, expires_delta=expires)
			return self.handle_response('OK', payload={'user': AccountController.user_object(student), 'refreshToken': refresh_token})

		return self.handle_response('No User Found or Permission Denied')

	def update_staff_account(self, id):
		admin = self.admin_repo.find_first(id=id, is_deleted=False)

		first_name, last_name, email, is_lecturer = self.request_params('first_name', 'last_name', 'email', 'is_lecturer')

		if admin:
			updates = {}

			if first_name:
				updates['first_name'] = first_name

			if last_name:
				updates['last_name'] = last_name

			if type(is_lecturer) == bool:
				updates['is_lecturer'] = is_lecturer

			if email and admin.email != email:
				if self.admin_repo.find_first(email=email):
					return self.handle_response('Email Already In Use', status_code=400)
				updates['email'] = email

			if len(updates) == 0:
				return self.handle_response('No Changes Made - No Parameters To Update', status_code=403)

			admin = self.admin_repo.update(admin, **updates)
			admin_object = {**admin.serialize(excluded=['password'])}
			expires = timedelta(days=30)
			refresh_token = create_access_token(identity=admin_object, expires_delta=expires)
			return self.handle_response('OK', payload={'user': AccountController.user_object(admin), 'refreshToken': refresh_token})

		return self.handle_response('No User Found or Permission Denied')

	def fetch_student_account(self, id, admin=False):
		user_id = self.user('id')
		if admin:
			user_id = id

		user = self.student_repo.find_first(id=user_id, is_deleted=False)
		if user:
			return self.handle_response('OK', payload={'account': AccountController.user_object(user)})
		return self.handle_response('Invalid ID Passed', status_code=400)

	def fetch_my_admin_account(self):
		user_id = self.user('id')
		user = self.student_repo.find_first(id=user_id, is_deleted=False)
		if user:
			return self.handle_response('OK', payload={'account': AccountController.user_object(user)})
		return self.handle_response('Invalid ID Passed or Permission Denied', status_code=400)

	def fetch_admin_account(self, id):
		admin_user = self.admin_repo.find_first(id=id, is_deleted=False)
		if admin_user:
			return self.handle_response('OK', payload={'account': AccountController.user_object(admin_user)})
		return self.handle_response('Invalid ID Passed', status_code=400)

	def verify_student(self, id, admin=False):
		student_id = self.user('id')
		if admin:
			student_id = id

		student = self.student_repo.find_first(id=student_id, is_deleted=False)

		if student:
			if not student.is_verified:
				student = self.student_repo.update(student, **{'is_verified': True})
				return self.handle_response('OK', payload={'account': AccountController.user_object(student)})

			return self.handle_response('User Account Already Active', status_code=403)

		return self.handle_response('No User Found or Invalid User ID')

		pass

	def toggle_premium_student(self, id, admin=False, confirm=True):
		student_id = self.user('id')
		if admin:
			student_id = id

		student = self.student_repo.find_first(id=student_id, is_deleted=False)

		if confirm and student.is_premium:
			return self.handle_response('Student Already Premium User')
		if not confirm and not student.is_premium:
			return self.handle_response('Student Not A Premium User')

		if student:
			student = self.student_repo.update(student, **{'is_premium': confirm})
			return self.handle_response('OK', payload={'account': AccountController.user_object(student)})

		return self.handle_response('No User Found or Invalid User ID')
		pass

	def fetch_list(self, account_type):
		status, = self.get_params('status')

		filter_by = {}

		if status and type(status) == bool:
			filter_by['status'] = status

		if account_type == 'student':
			if len(filter_by) > 0:
				users = self.student_repo.filter_by(is_deleted=False, **filter_by)
			else:
				users = self.student_repo.filter_by(is_deleted=False)
		elif account_type == 'admin':
			if len(filter_by) > 0:
				users = self.admin_repo.filter_by(is_deleted=False, **filter_by)
			else:
				users = self.admin_repo.filter_by(is_deleted=False)
		else:
			return self.handle_response('Invalid Account Type Passed', status_code=400)

		users_list = [AccountController.user_object(user) for user in users.items]

		if account_type == 'student':
			meta_items = self.student_repo.pagination_meta(users)
		elif account_type == 'admin':
			meta_items = self.admin_repo.pagination_meta(users)

		return self.handle_response('OK', payload={'accounts': users_list, 'meta': meta_items})

	@staticmethod
	def user_object(user, with_timestamp=False):
		return {
			**user.serialize(with_timestamp=with_timestamp)
		}
