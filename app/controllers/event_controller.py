from app.controllers.base_controller import BaseController

from app.repositories.student_repo import StudentRepo
from app.repositories.admin_repo import AdminRepo
from app.repositories.event_repo import EventRepo
from app.repositories.student_event_repo import StudentEventRepo
from app.repositories.lecture_repo import LectureRepo
from app.repositories.lecture_admin_repo import LectureAdminRepo

from flask import render_template
from datetime import datetime, timedelta


class EventController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.student_repo = StudentRepo()
		self.admin_repo = AdminRepo()
		self.event_repo = EventRepo()
		self.student_event_repo = StudentEventRepo()
		self.lecture_repo = LectureRepo()
		self.lecture_admin_repo = LectureAdminRepo()

	""" MISC """

	@staticmethod
	def event_object(event, with_timestamp=False):
		event_obj = {
			# **event.serialize(excluded=['user_id', 'delivery_address'], with_timestamp=with_timestamp)
			**event.serialize(with_timestamp=with_timestamp),
			** {
				'lectures': [
					{**lecture.serialize()} for lecture in event.lectures
				]
			}
		}
		return event_obj
