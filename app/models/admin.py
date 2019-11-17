from .base_model import BaseModel, db


class Admin(BaseModel):
	__tablename__ = 'admins'
	
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	is_lecturer = db.Column(db.Boolean(), nullable=True, default=False)
	status = db.Column(db.Boolean(), nullable=True, default=True)
	auth_key = db.Column(db.String(255), nullable=True)

	lecture_admin = db.relationship('LectureAdmin')
