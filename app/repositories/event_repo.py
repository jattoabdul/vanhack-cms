from app.repositories.base_repo import BaseRepo
from app.models.event import Event

class EventRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Event)