from .base_model import BaseModel, db


class Event(BaseModel):
	__tablename__ = 'events'
	
	name = db.Column(db.String(255), nullable=False, unique=True)
	reference = db.Column(db.String(100), nullable=False, unique=True)
	desc = db.Column(db.Text(), nullable=True)

	student_event = db.relationship('StudentEvent')
	lectures = db.relationship('OrderLineItem', lazy=False)
