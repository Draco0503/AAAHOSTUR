from dataclasses import dataclass
from . import db


@dataclass()
class AcademicProfile(db.Model):
    __tablename__ = 'Academic_Profile'
    ID_ACADEMIC_PROFILE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    School = db.Column(db.String(512), nullable=False)
    Graduation_Date = db.Column(db.String(256), nullable=False)
    Promotion = db.Column(db.String(256))
    Id_Member = db.Column(db.Integer, db.ForeignKey('Member.ID_MEMBER'), nullable=False)
    Id_Qualification = db.Column(db.Integer, db.ForeignKey('Qualification.ID_QUALIFICATION'), nullable=False)

    member = db.relationship('Member', backref='academic_profiles')
    qualification = db.relationship('Qualification', backref='academic_profiles')