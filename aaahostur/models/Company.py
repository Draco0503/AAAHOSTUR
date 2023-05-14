from dataclasses import dataclass
from . import db


@dataclass()
class Company(db.Model):
    __tablename__ = "Company"
    ID_COMPANY = db.Column(db.Integer, db.ForeignKey("User.ID_USER"), primary_key=True)
    Type = db.Column(db.String(512), nullable=False)
    CIF = db.Column(db.String(512), nullable=False, unique=True)
    Address = db.Column(db.String(512), nullable=True)
    CP = db.Column(db.String(512), nullable=True)
    City = db.Column(db.String(512), nullable=True)
    Province = db.Column(db.String(512), nullable=True)
    Contact_Name = db.Column(db.String(512), nullable=False)
    Contact_Phone = db.Column(db.String(512), nullable=False)
    Contact_Email = db.Column(db.String(512), nullable=False)
    Description = db.Column(db.String(512), nullable=True)
    Verify = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=True)

    Id_Company_Parent = db.Column(db.Integer, db.ForeignKey("Company.ID_COMPANY"), nullable=True)
    Id_User_Creator = db.Column(db.Integer, db.ForeignKey("User.ID_USER"))

    company_account = db.relationship("Company_Account", backref="Company", lazy=True)
