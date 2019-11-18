from .base_model import BaseModel, db
from datetime import datetime


class Lecture(BaseModel):
	__tablename__ = 'lectures'

	event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
	topic = db.Column(db.String(255), nullable=False)
	desc = db.Column(db.Text(), nullable=True)
	zoom_link = db.Column(db.String(255), nullable=True)
	datetime = db.Column(db.DateTime(), nullable=True)

	lecture_admins = db.relationship('LectureAdmin')
	event = db.relationship('Event', foreign_keys=[event_id])
