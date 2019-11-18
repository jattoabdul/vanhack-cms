from .base_model import BaseModel, db


class Event(BaseModel):
	__tablename__ = 'events'
	
	name = db.Column(db.String(255), nullable=False, unique=True)
	desc = db.Column(db.Text(), nullable=True)
	status = db.Column(db.Boolean(), nullable=True, default=True)

	student_event = db.relationship('StudentEvent')
	lectures = db.relationship('Lecture', lazy=False)
