from app.controllers.base_controller import BaseController

from app.repositories.student_repo import StudentRepo
from app.repositories.admin_repo import AdminRepo
from app.repositories.event_repo import EventRepo
from app.repositories.student_event_repo import StudentEventRepo
from app.repositories.lecture_repo import LectureRepo
from app.repositories.lecture_admin_repo import LectureAdminRepo

# from flask import render_template
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

	# admin fetch all events
	# student fetch all events (if student.is_premium and event.status is true)
	def fetch_events(self, student=False):
		filters = {'is_deleted': False}
		if student:
			student_id = self.user('id')
			student = self.student_repo.find_first(id=student_id, is_deleted=False, is_premium=True)
			if not student:
				return self.handle_response('No Student Found Or Permission Denied')
			filters['status'] = True
		events = self.event_repo.filter_by(**filters)
		event_list = [event.serialize() for event in events.items]
		return self.handle_response('OK', payload={'events': event_list, 'meta': self.event_repo.pagination_meta(events)})

	# admin fetch single event
	# student fetch single event
	def fetch_single_event(self, event_id, student=False):
		if student:
			student_id = self.user('id')
			student = self.student_repo.find_first(id=student_id, is_deleted=False, is_premium=True)
			if not student:
				return self.handle_response('No Student Found Or Permission Denied')
			if self.student_event_repo.filter_and_count(event_id=event_id, student_id=student_id) <= 0:
				return self.handle_response('No Event Found For This Student')

		event = self.event_repo.find_first(id=event_id, is_deleted=False)
		if event:
			return self.handle_response('OK', payload={'event': event.serialize()})
		return self.handle_response('Invalid or Missing Event Id')

	""" ADMIN ONLY ACTIONS """
	# admin create event
	def create_event(self):
		name, desc = self.request_params('name', 'desc')
		if self.event_repo.filter_and_count(name=name) > 0:
			return self.handle_response('Event With Name Already Exists', status_code=400)
		event = self.event_repo.new_event(name=name, desc=desc)
		if event:
			return self.handle_response('OK', payload={
				'event': {**event.serialize()}
			})
		return self.handle_response('Internal Application Error. Please Try Again', status_code=400)

	# admin update event
	def update_event(self, event_id):
		event = self.event_repo.find_first(id=event_id, is_deleted=False)

		name, desc, status = self.request_params('name', 'desc', 'status')

		if event:
			updates = {}

			if name:
				updates['name'] = name

			if desc:
				updates['desc'] = desc

			if status and type(status) == bool:
				updates['status'] = status

			if len(updates) == 0:
				return self.handle_response('No Changes Made - No Parameters To Update', status_code=403)

			self.event_repo.update(event, **updates)
			return self.handle_response('OK', payload={'event': event.serialize()})
		return self.handle_response('No Event Found or Permission Denied')

	""" STUDENT ONLY ACTIONS """
	# student fetch all events which he/she has subscribed to (if student.is_premium)
	def fetch_my_events(self):
		student_id = self.user('id')
		student = self.student_repo.find_first(id=student_id, is_deleted=False, is_premium=True)
		if not student:
			return self.handle_response('No Student Found Or Permission Denied')
		student_events = self.student_event_repo.get_unpaginated(student_id=student_id)
		event_list_ids = [student_event.event_id for student_event in student_events]
		events = self.event_repo.fetch_events(event_list_ids)
		event_list = [event.serialize() for event in events]
		return self.handle_response('OK', payload={'events': event_list})

	# student subscribe to event
	def subscribe_to_event(self, event_id):
		student_id = self.user('id')
		student = self.student_repo.find_first(id=student_id, is_deleted=False, is_premium=True, is_verified=True)
		if not student:
			return self.handle_response('No Student Found Or Permission Denied')
		event = self.event_repo.find_first(id=event_id, is_deleted=False)
		if event:
			student_event = self.student_event_repo.new_student_event(event_id=event_id, student_id=student_id)
			if student_event:
				return self.handle_response('OK', payload={
					'msg': 'Student Subscribed Successfully',
					'student': student.serialize(),
					'event': event.serialize()
				}, status_code=201)
			return self.handle_response('Application Error', status_code=500)
		return self.handle_response('No Event Found or Permission Denied')

	# student unsubscribe from event
	def unsubscribe_from_event(self, event_id):
		student_id = self.user('id')
		student = self.student_repo.find_first(id=student_id, is_deleted=False, is_premium=True)
		if not student:
			return self.handle_response('No Student Found Or Permission Denied')
		event = self.event_repo.find_first(id=event_id, is_deleted=False)
		if event:
			student_event = self.student_event_repo.find_first(event_id=event_id, student_id=student_id)
			if student_event:
				student_event.delete()
				return self.handle_response('Student Unsubscribed Successfully')
			return self.handle_response('Student Not Previously Subscribed To Event', status_code=400)
		return self.handle_response('No Event Found or Permission Denied')

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
