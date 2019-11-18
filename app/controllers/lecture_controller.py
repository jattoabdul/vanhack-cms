from app.controllers.base_controller import BaseController

from app.repositories.student_repo import StudentRepo
from app.repositories.admin_repo import AdminRepo
from app.repositories.event_repo import EventRepo
from app.repositories.student_event_repo import StudentEventRepo
from app.repositories.lecture_repo import LectureRepo
from app.repositories.lecture_admin_repo import LectureAdminRepo

from flask import render_template
from datetime import datetime, timedelta


class LectureController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		self.student_repo = StudentRepo()
		self.admin_repo = AdminRepo()
		self.event_repo = EventRepo()
		self.student_event_repo = StudentEventRepo()
		self.lecture_repo = LectureRepo()
		self.lecture_admin_repo = LectureAdminRepo()

	""" Admin BluePrints """
	# admin create event lecture with lecturers
	def create_lecture(self):
		event_id, topic, desc, zoom_link, datetime = self.request_params('event_id', 'topic', 'desc', 'zoom_link', 'datetime')

		if self.lecture_repo.filter_and_count(event_id=event_id, topic=topic) > 0:
			return self.handle_response('Lecture With Topic Already Exists For Current Event', status_code=400)
		if not datetime:
			return self.handle_response('Lecture Must Have a DateTime', status_code=400)

		lecture = self.lecture_repo.new_lecture(topic=topic, desc=desc, zoom_link=zoom_link, datetime=datetime)
		if lecture:
			return self.handle_response('OK', payload={
				'lecture': {**lecture.serialize()}
			})
		return self.handle_response('Internal Application Error. Please Try Again', status_code=400)

	# admin update event lecture
	def update_lecture(self, lecture_id):
		lecture = self.lecture_repo.find_first(id=lecture_id, is_deleted=False)

		topic, desc, zoom_link, datetime = self.request_params('topic', 'desc', 'zoom_link', 'datetime')

		if lecture:
			updates = {}

			if topic:
				updates['topic'] = topic

			if desc:
				updates['desc'] = desc

			if zoom_link:
				updates['zoom_link'] = zoom_link

			if datetime:
				updates['datetime'] = datetime

			if len(updates) == 0:
				return self.handle_response('No Changes Made - No Parameters To Update', status_code=403)

			self.lecture_repo.update(lecture, **updates)
			return self.handle_response('OK', payload={'lecture': lecture.serialize()})
		return self.handle_response('No Lecture Found or Permission Denied')

	# admin add lecturers to an event lecture
	def add_lecturer_to_lecture(self, lecture_id):
		lecturer_ids, = self.request_params('lecturer_ids')

		lecture = self.lecture_repo.find_first(id=lecture_id, is_deleted=False)
		if not lecture:
			return self.handle_response('Lecture Not Found Or Permission Denied')

		if type(lecturer_ids) is not list:
			return self.handle_response('Lecturer IDs must be list of lecturer ids', status_code=400)

		# Validate lecturers exist
		for lecturer_id in lecturer_ids:
			lecturer = self.admin_repo.find_first(id=lecturer_id, is_deleted=False, is_lecturer=True)
			if not lecturer:
				return self.handle_response(f'Admin User with ID {lecturer_id} Not Found or Must be A Lecturer', status_code=400)

		lecturers_mappings = []
		for lecturer_id in lecturer_ids:
			lecturers_mappings.append({'lecture_id': lecture_id, 'admin_id': lecturer_id})

		self.lecture_admin_repo.bulk_insert(lecturers_mappings)
		return self.handle_response('Lecturers Added Successfully')

	# admin remove lecturers from an event lecture
	# admin fetch single event lecture with lecturers
	# admin fetch all event lectures with lecturers
	# admin fetch list of all lecturers

	""" Student BluePrints """
	# student fetch single lecture of event which he/she has subscribed to (if student.is_premium)
	# student fetch all lectures of event which he/she has subscribed to (if student.is_premium)

	""" MISC """
	@staticmethod
	def lecture_object(lecture, with_timestamp=False):
		lecture_obj = {
			**lecture.serialize(with_timestamp=with_timestamp)
			# **{
			# 	'lecturers': [lecturer for lecturer in lecture.lecture_admins],
			# 	'event': lecture.event.serialize(with_timestamp=False)
			# }
		}
		return lecture_obj
