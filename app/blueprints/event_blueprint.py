from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.event_controller import EventController

url_prefix = '{}'.format(BaseBlueprint.base_url_prefix)
event_blueprint = Blueprint('event', __name__, url_prefix=url_prefix)

event_controller = EventController(request)

""" Admin BluePrints """


# admin create event
@event_blueprint.route('/admin/events', methods=['POST'])
@Security.validator(['name|required'])
def create_event():
	return event_controller.create_event()


# admin update event
@event_blueprint.route('/admin/events/<int:event_id>', methods=['PUT', 'PATCH'])
def update_event(event_id):
	return event_controller.update_event(event_id)


# admin fetch all events
@event_blueprint.route('/admin/events', methods=['GET'])
def admin_fetch_events():
	return event_controller.fetch_events(student=False)


# admin fetch single event
@event_blueprint.route('/admin/events/<int:event_id>', methods=['GET'])
def admin_fetch_event(event_id):
	return event_controller.fetch_single_event(event_id, student=False)


""" Student BluePrints """
# student fetch single event
@event_blueprint.route('/student/events/<int:event_id>', methods=['GET'])
def student_fetch_event(event_id):
	return event_controller.fetch_single_event(event_id, student=True)


# student fetch all events (if student.is_premium and event.status is true)
@event_blueprint.route('/events', methods=['GET'])
def student_fetch_events():
	return event_controller.fetch_events(student=True)


# student fetch all events which he/she has subscribed to (if student.is_premium)
@event_blueprint.route('/student/events/personal', methods=['GET'])
def student_fetch_personal_events():
	return event_controller.fetch_my_events()


# student subscribe to event
@event_blueprint.route('/student/events/<int:event_id>/subscribe', methods=['POST'])
def student_subscribe_to_event(event_id):
	return event_controller.subscribe_to_event(event_id)

# student unsubscribe from event
@event_blueprint.route('/student/events/<int:event_id>/unsubscribe', methods=['POST'])
def student_unsubscribe_to_event(event_id):
	return event_controller.unsubscribe_from_event(event_id)
