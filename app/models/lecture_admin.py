from .base_model import BaseModel, db

class LectureAdmin(BaseModel):
	__tablename__ = 'lecture_admins'
	
	lecture_id = db.Column(db.Integer(), db.ForeignKey('lectures.id'))
	admin_id = db.Column(db.Integer(), db.ForeignKey('admins.id'))

	lecture = db.relationship('Lecture', foreign_keys=[lecture_id])
	admin = db.relationship('Admin', foreign_keys=[admin_id])
