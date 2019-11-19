from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.lecture_controller import LectureController


url_prefix = '{}'.format(BaseBlueprint.base_url_prefix)
lecture_blueprint = Blueprint('lecture', __name__, url_prefix=url_prefix)

lecture_controller = LectureController(request)

""" Admin BluePrints """
@lecture_blueprint.route('/admin/events/<int:event_id>/lectures', methods=['POST'])
@Auth.has_permission('admin')
def admin_create_event_lecture(event_id):
	return lecture_controller.create_lecture(event_id)


@lecture_blueprint.route('/admin/events/<int:event_id>/lectures/<int:lecture_id>', methods=['PUT', 'PATCH'])
@Auth.has_permission('admin')
def admin_update_event_lecture(event_id, lecture_id):
	return lecture_controller.update_lecture(event_id, lecture_id)


@lecture_blueprint.route('/admin/events/<int:event_id>/lectures/<int:lecture_id>/lecturers/add', methods=['POST'])
@Auth.has_permission('admin')
def admin_add_lecturers_to_event_lecture(event_id, lecture_id):
	return lecture_controller.add_lecturers_to_lecture(event_id, lecture_id)


@lecture_blueprint.route('/admin/events/<int:event_id>/lectures/<int:lecture_id>/lecturers/remove', methods=['DELETE'])
@Auth.has_permission('admin')
def admin_remove_lecturers_to_event_lecture(event_id, lecture_id):
	return lecture_controller.remove_lecturers_from_lecture(event_id, lecture_id)


@lecture_blueprint.route('/admin/events/<int:event_id>/lectures/<int:lecture_id>', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_single_event_lecture(event_id, lecture_id):
	return lecture_controller.fetch_single_event_lecture(event_id, lecture_id)


@lecture_blueprint.route('/admin/events/<int:event_id>/lectures', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_all_event_lectures(event_id):
	return lecture_controller.fetch_all_event_lectures(event_id)


@lecture_blueprint.route('/admin/lectures', methods=['GET'])
@Auth.has_permission('admin')
def admin_fetch_all_lectures():
	return lecture_controller.fetch_all_lectures()


""" Student BluePrints """
@lecture_blueprint.route('/student/events/<int:event_id>/lectures/<int:lecture_id>', methods=['GET'])
@Auth.has_permission('student')
def student_fetch_single_event_lecture(event_id, lecture_id):
	return lecture_controller.fetch_single_event_lecture_for_student(event_id, lecture_id)


@lecture_blueprint.route('/student/events/<int:event_id>/lectures', methods=['GET'])
@Auth.has_permission('student')
def student_fetch_all_event_lectures(event_id):
	return lecture_controller.fetch_all_event_lectures_for_student(event_id)
