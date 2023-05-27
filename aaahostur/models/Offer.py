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
    Contact_Name_2 = db.Column(db.String(512), nullable=True)
    Contact_Phone_2 = db.Column(db.String(512), nullable=True)
    Contact_Email_2 = db.Column(db.String(512), nullable=True)
    Verify = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=True)

    Id_Company = db.Column(db.Integer, db.ForeignKey('Company.ID_COMPANY'))
    Id_User_Verify = db.Column(db.Integer, db.ForeignKey('User.ID_USER'))

    def to_json(self):
        return {'id_offer': self.ID_OFFER,
                'company_name': self.Company_Name,
                'address': self.Address,
                'contact_name': self.Contact_Name,
                'contact_phone': self.Contact_Phone,
                'contact_email': self.Contact_Email,
                'contact_name_2': self.Contact_Name_2,
                'contact_phone_2': self.Contact_Phone_2,
                'contact_email_2': self.Contact_Email_2,
                'verify': self.Verify,
                'active': self.Active,
                'id_company': self.Id_Company,
                'id_user_verify': self.Id_User_Verify
                }