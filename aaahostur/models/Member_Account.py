from dataclasses import dataclass
from . import db


@dataclass()
class Member_Account(db.Model):
    __tablename__ = "Member_Account"
    ID_MEMBER_ACCOUNT = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Account_Holder = db.Column(db.String(512), nullable=False)
    Account_Number = db.Column(db.String(512), nullable=False, unique=True)
    SEPA_Form = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=False)
    
    Id_Member = db.Column(db.String(36), db.ForeignKey("Member.ID_MEMBER"), nullable=False)
    Id_User_Verify = db.Column(db.String(36), db.ForeignKey("User.ID_USER"))

    def to_json(self):
        return {'id_member_account': self.ID_MEMBER_ACCOUNT,
                'account_holder': self.Account_Holder,
                'account_number': self.Account_Number,
                'sepa_form': self.SEPA_Form,
                'active': self.Active,
                'id_member': self.Id_Member,
                'id_user_verify': self.Id_User_Verify
                }