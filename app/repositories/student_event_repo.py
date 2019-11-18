from app.repositories.base_repo import BaseRepo
from app.models.student_event import StudentEvent

class StudentEventRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, StudentEvent)

	def new_student_event(self, event_id, student_id):
		student_event = StudentEvent(event_id=event_id, student_id=student_id)
		student_event.save()
		return student_event
