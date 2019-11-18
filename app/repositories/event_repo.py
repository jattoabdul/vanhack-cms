from app.repositories.base_repo import BaseRepo
from app.models.event import Event


class EventRepo(BaseRepo):

	def __init__(self):
		BaseRepo.__init__(self, Event)

	def new_event(self, name, desc):
		event = Event(name=name, desc=desc)
		event.save()
		return event

	def fetch_events(self, ids: list):
		if type(ids) is not list:
			raise Exception('ids must be list')
		return self._model.query.filter(Event.id.in_(ids)).all()
