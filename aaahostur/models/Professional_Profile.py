from dataclasses import dataclass
from . import db


@dataclass()
class ProfessionalProfile(db.Model):
    __tablename__ = 'Professional_Profile'

    ID_PROFESSIONAL_PROFILE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Workplace = db.Column(db.String(512), nullable=False)
    Address = db.Column(db.String(512), nullable=False)
    Position = db.Column(db.String(512), nullable=False)
    Join_Date = db.Column(db.String(256), nullable=False)
    Finish_Date = db.Column(db.String(256), default='CURRENT')
    Id_Member = db.Column(db.Integer, db.ForeignKey('Member.ID_MEMBER'), nullable=False)

    member = db.relationship('Member', backref='professional_profiles')
