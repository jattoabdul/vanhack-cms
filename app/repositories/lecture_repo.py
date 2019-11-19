from app.repositories.base_repo import BaseRepo
from app.models.lecture import Lecture


class LectureRepo(BaseRepo):
	
	def __init__(self):
		BaseRepo.__init__(self, Lecture)

	def new_lecture(self, event_id, topic, desc, zoom_link, datetime):
		lecture = Lecture(event_id=event_id, topic=topic, desc=desc, zoom_link=zoom_link, datetime=datetime)
		lecture.save()
		return lecture
