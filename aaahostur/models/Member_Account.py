from dataclasses import dataclass
from . import db


@dataclass()
class Member_Account(db.Model):
    __tablename__ = "Member_Account"
    ID_MEMBER_ACCOUNT = db.Column(db.Integer, primary_key=True)
    Account_Holder = db.Column(db.String(512), nullable=False)
    Account_Number = db.Column(db.String(512), nullable=False, unique=True)
    SEPA_Form = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=False)

    Id_Member = db.Column(db.Integer, db.ForeignKey("Member.ID_MEMBER"), nullable=False)
    Id_User_Verify = db.Column(db.Integer, db.ForeignKey("User.ID_USER"))
