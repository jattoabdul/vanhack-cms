from app.repositories.base_repo import BaseRepo
from app.models.student import Student
from uuid import uuid4
from sqlalchemy.sql.expression import or_


class StudentRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Student)

	def new_user(self, first_name, last_name, email, password, is_verified, is_premium):
		user = Student(
			first_name=first_name, last_name=last_name, email=email, password=password,
			is_verified=is_verified, is_premium=is_premium
		)
		user.save()
		return user

	@staticmethod
	def refresh_auth_key(user):
		auth_key = str(uuid4())
		user.auth_key = auth_key
		user.save()
		return user

	def name_or_email_like(self, query_keyword):
		query_keyword = f'%{query_keyword}%'
		return self._model.query.filter(or_((Student.email.ilike(query_keyword)), (Student.first_name.ilike(query_keyword)),
											(Student.last_name.ilike(query_keyword)))).paginate(error_out=False)
