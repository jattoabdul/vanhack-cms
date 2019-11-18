from app.blueprints.base_blueprint import Blueprint, BaseBlueprint, request, Security, Auth
from app.controllers.lecture_controller import LectureController


url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
lecture_blueprint = Blueprint('lecture', __name__, url_prefix=url_prefix)

lecture_controller = LectureController(request)

""" Admin BluePrints """
# admin create event lecture
# admin update event lecture
# admin fetch single event lecture
# admin fetch all event lectures

""" Student BluePrints """
# student fetch single lecture of event which he/she has subscribed to (if student.is_premium)
# student fetch all lectures of event which he/she has subscribed to (if student.is_premium)
