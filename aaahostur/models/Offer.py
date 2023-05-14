from dataclasses import dataclass
from . import db


@dataclass()
class Offer(db.Model):
    __tablename__ = "Offer"
    ID_OFFER = db.Column(db.Integer, primary_key=True)
    Company_Name = db.Column(db.String(512), nullable=False)
    Address = db.Column(db.String(512), nullable=False)
    Contact_Name = db.Column(db.String(512), nullable=False)
    Contact_Phone = db.Column(db.String(512), nullable=False)
    Contact_Email = db.Column(db.String(512), nullable=False)
    Contact_Name_2 = db.Column(db.String(512))
    Contact_Phone_2 = db.Column(db.String(512))
    Contact_Email_2 = db.Column(db.String(512))
    Verify = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=True)

    Id_Company = db.Column(db.Integer, db.ForeignKey('Company.ID_COMPANY'))
    Id_User_Verify = db.Column(db.Integer, db.ForeignKey('User.ID_USER'))
