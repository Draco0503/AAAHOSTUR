from dataclasses import dataclass
from . import db


@dataclass()
class Role(db.Model):
    __tablename__ = "Role"
    ID_ROLE = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Description = db.Column(db.String(512))
    CanVerifyMember = db.Column(db.Boolean, default=False)
    CanVerifyCompany = db.Column(db.Boolean, default=False)
    CanVerifyAdmin = db.Column(db.Boolean, default=False)
    CanVerifyOffer = db.Column(db.Boolean, default=False)
    CanVerifyReview = db.Column(db.Boolean, default=False)
    CanSeeOffer = db.Column(db.Boolean, default=False)
    CanApplyOffer = db.Column(db.Boolean, default=False)
    CanMakeOffer = db.Column(db.Boolean, default=False)
    CanSeeSection = db.Column(db.Boolean, default=False)
    CanMakeSection = db.Column(db.Boolean, default=False)
    CanActiveMember = db.Column(db.Boolean, default=False)
    CanActiveCompany = db.Column(db.Boolean, default=False)
    CanActiveSection = db.Column(db.Boolean, default=False)
    CanActiveOffer = db.Column(db.Boolean, default=False)
    CanActiveReview = db.Column(db.Boolean, default=False)
    CanActiveCompanyBankAcc = db.Column(db.Boolean, default=False)
    CanActiveMemberBankAcc = db.Column(db.Boolean, default=False)
    CanSeeReview = db.Column(db.Boolean, default=False)
    CanMakeReview = db.Column(db.Boolean, default=False)

    User = db.relationship("User", backref="Role", lazy=True)
