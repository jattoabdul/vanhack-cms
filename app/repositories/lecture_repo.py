from app.repositories.base_repo import BaseRepo
from app.models.lecture import Lecture

class LectureRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Lecture)