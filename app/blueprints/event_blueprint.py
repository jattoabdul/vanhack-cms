from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.event_controller import EventController

url_prefix = '{}'.format(BaseBlueprint.base_url_prefix)
event_blueprint = Blueprint('event', __name__, url_prefix=url_prefix)

event_controller = EventController(request)

""" Admin BluePrints """


@event_blueprint.route('/admin/events', methods=['POST'])
@Security.validator(['name|required'])
@Auth.has_permission('admin')
def create_event():
	return event_controller.create_event()


@event_blueprint.route('/admin/events/<int:event_id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def update_event(event_id):
	return event_controller.update_event(event_id)


@event_blueprint.route('/admin/events', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_events():
	return event_controller.fetch_events(student=False)


@event_blueprint.route('/admin/events/<int:event_id>', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_event(event_id):
	return event_controller.fetch_single_event(event_id, student=False)


""" Student BluePrints """
@event_blueprint.route('/student/events/<int:event_id>', methods=['GET'])
@Auth.has_permission('student')
def student_fetch_event(event_id):
	return event_controller.fetch_single_event(event_id, student=True)


@event_blueprint.route('/events', methods=['GET'])
@Auth.has_permission('student')
def student_fetch_events():
	return event_controller.fetch_events(student=True)


@event_blueprint.route('/student/events/personal', methods=['GET'])
@Auth.has_permission('student')
def student_fetch_personal_events():
	return event_controller.fetch_my_events()


@event_blueprint.route('/student/events/<int:event_id>/subscribe', methods=['POST'])
@Auth.has_permission('student')
def student_subscribe_to_event(event_id):
	return event_controller.subscribe_to_event(event_id)


@event_blueprint.route('/student/events/<int:event_id>/unsubscribe', methods=['POST'])
@Auth.has_permission('student')
def student_unsubscribe_to_event(event_id):
	return event_controller.unsubscribe_from_event(event_id)
