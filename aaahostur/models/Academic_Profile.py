from dataclasses import dataclass
from . import db


@dataclass()
class Academic_Profile(db.Model):
    __tablename__ = 'Academic_Profile'
    ID_ACADEMIC_PROFILE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    School = db.Column(db.String(512), nullable=False)
    Graduation_Date = db.Column(db.String(256), nullable=False)
    Promotion = db.Column(db.String(256))
    Id_Member = db.Column(db.Integer, db.ForeignKey('Member.ID_MEMBER'), nullable=False)
    Id_Qualification = db.Column(db.Integer, db.ForeignKey('Qualification.ID_QUALIFICATION'), nullable=False)

    # member = db.relationship('Member', backref='Academic_Profile')
    qualification = db.relationship('Qualification', backref='Academic_Profile')

    def to_json(self):
        return {'id_academic_profile': self.ID_ACADEMIC_PROFILE,
                'school': self.School,
                'graduation_date': self.Graduation_Date,
                'promotion': self.Promotion,
                'id_member': self.Id_Member,
                'id_qualification': self.Id_Qualification
                }