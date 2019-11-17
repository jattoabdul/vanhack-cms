from .base_model import BaseModel, db
from datetime import datetime


class Lecture(BaseModel):
	__tablename__ = 'lectures'

	event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
	topic = db.Column(db.String(255), nullable=False, unique=True)
	reference = db.Column(db.String(100), nullable=False, unique=True)
	desc = db.Column(db.Text(), nullable=True)
	zoom_link = db.Column(db.String(255), nullable=True)
	datetime = db.Column(db.DateTime(), default=datetime.now())

	lecture_admin = db.relationship('LectureAdmin')
	event = db.relationship('Event', foreign_keys=[event_id])
