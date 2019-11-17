from app.repositories.base_repo import BaseRepo
from app.models.lecture_admin import LectureAdmin

class LectureAdminRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, LectureAdmin)