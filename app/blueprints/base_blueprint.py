from flask import Blueprint, request
from app.utils.security import Security
from app.utils.auth import Auth


class BaseBlueprint:
	
	base_url_prefix = '/api/v1'
	
	def __init__(self, app):
		self.app = app
	
	def register(self):
		
		''' Register All App Blue Prints Here '''
		
		from app.blueprints.home_blueprint import home_blueprint
		self.app.register_blueprint(home_blueprint)

		from app.blueprints.auth_blueprint import auth_blueprint
		self.app.register_blueprint(auth_blueprint)

		from app.blueprints.account_blueprint import account_blueprint
		self.app.register_blueprint(account_blueprint)

		from app.blueprints.event_blueprint import event_blueprint
		self.app.register_blueprint(event_blueprint)

		from app.blueprints.lecture_blueprint import lecture_blueprint
		self.app.register_blueprint(lecture_blueprint)

		from app.blueprints.search_blueprint import search_blueprint
		self.app.register_blueprint(search_blueprint)
