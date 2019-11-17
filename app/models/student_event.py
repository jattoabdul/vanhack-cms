from .base_model import BaseModel, db


class StudentEvent(BaseModel):
	__tablename__ = 'student_events'
	
	event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
	student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))

	event = db.relationship('Event', foreign_keys=[event_id])
	student = db.relationship('Student', foreign_keys=[student_id])
