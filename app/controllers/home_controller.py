from flask import request
from config import get_env
from app.controllers.base_controller import BaseController

class HomeController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		
	def home_page(self):
		return self.handle_response('OK', payload={'vessel': f'Welcome Message v1 {request.headers}'})

	def api_status(self):
		return self.handle_response('OK', payload={
			'services': { 'api': 'OK', 'db': 'OK' },
			'env': get_env('APP_ENV')
		})
