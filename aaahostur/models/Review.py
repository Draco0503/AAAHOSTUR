from dataclasses import dataclass
from . import db


@dataclass()
class Review(db.Model):
    __tablename__ = 'Review'

    ID_REVIEW = db.Column(db.Integer, primary_key=True)
    Score = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.String(512))
    Business_Sender = db.Column(db.Integer, nullable=False)
    Verify = db.Column(db.Boolean, default=False, nullable=False)
    Active = db.Column(db.Boolean, default=True, nullable=False)
    Id_User_Verify = db.Column(db.Integer, db.ForeignKey('User.ID_USER'))
    Id_Company = db.Column(db.Integer, db.ForeignKey('Company.ID_COMPANY'))
    Id_Member = db.Column(db.Integer, db.ForeignKey('Member.ID_MEMBER'))

    user_verify = db.relationship('User', backref='reviews')
    company = db.relationship('Company', backref='reviews')
    member = db.relationship('Member', backref='reviews')

    def to_json(self):
        return {'id_review': self.ID_REVIEW,
                'score': self.Score,
                'description': self.Description,
                'business_sender': self.Business_Sender,
                'verify': self.Verify,
                'active': self.Active,
                'id_user_verify': self.Id_User_Verify,
                'id_company': self.Id_Company,
                'id_member': self.Id_Member
                }