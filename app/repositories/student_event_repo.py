from app.repositories.base_repo import BaseRepo
from app.models.student_event import StudentEvent

class StudentEventRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, StudentEvent)