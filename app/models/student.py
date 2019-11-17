from .base_model import BaseModel, db


class Student(BaseModel):
	__tablename__ = 'students'
	
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	is_verified = db.Column(db.Boolean(), nullable=True, default=False)
	is_premium = db.Column(db.Boolean(), nullable=True, default=False)
	status = db.Column(db.Boolean(), nullable=True, default=True)
	auth_key = db.Column(db.String(255), nullable=True)

	student_event = db.relationship("StudentEvent")
