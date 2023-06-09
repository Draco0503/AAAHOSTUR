from dataclasses import dataclass
from . import db


@dataclass()
class Role(db.Model):
    __tablename__ = "Role"
    ID_ROLE = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    # API PRIVILEGES
    CanSeeApiRole = db.Column(db.Boolean, default=False)
    CanSeeApiLanguage = db.Column(db.Boolean, default=False)
    CanSeeApiJobCategory = db.Column(db.Boolean, default=False)
    CanSeeApiQualification = db.Column(db.Boolean, default=False)
    CanSeeApiUser = db.Column(db.Boolean, default=False)
    CanSeeApiSection = db.Column(db.Boolean, default=False)
    CanSeeApiCompany = db.Column(db.Boolean, default=False)
    CanSeeApiMember = db.Column(db.Boolean, default=False)
    CanSeeApiOffer = db.Column(db.Boolean, default=False)
    CanSeeApiReview = db.Column(db.Boolean, default=False)
    # CLASSIFICATION
    IsAAAHOSTUR = db.Column(db.Boolean, default=False)
    IsMember = db.Column(db.Boolean, default=False)
    IsCompany = db.Column(db.Boolean, default=False)

    User = db.relationship("User", backref="Role", lazy=True)

    def to_json(self):
        return {'id_role': self.ID_ROLE,
                'name': self.Name,
                'description': self.Description,
                'canVerifyMember': self.CanVerifyMember,
                'canVerifyCompany': self.CanVerifyCompany,
                'canVerifyAdmin': self.CanVerifyAdmin,
                'canVerifyOffer': self.CanVerifyOffer,
                'canVerifyReview': self.CanVerifyReview,
                'canSeeOffer': self.CanSeeOffer,
                'canApplyOffer': self.CanApplyOffer,
                'canMakeOffer': self.CanMakeOffer,
                'canSeeSection': self.CanSeeSection,
                'canMakeSection': self.CanMakeSection,
                'canActiveMember': self.CanActiveMember,
                'canActiveCompany': self.CanActiveCompany,
                'canActiveSection': self.CanActiveSection,
                'canActiveOffer': self.CanActiveOffer,
                'canActiveReview': self.CanActiveReview,
                'canActiveCompanyBankAcc': self.CanActiveCompanyBankAcc,
                'canActiveMemberBankAcc': self.CanActiveMemberBankAcc,
                'canSeeReview': self.CanSeeReview,
                'canMakeReview': self.CanMakeReview,
                # API PRIVILEGES
                'canSeeApiRole': self.CanSeeApiRole,
                'canSeeApiLanguage': self.CanSeeApiLanguage,
                'canSeeApiJobCategory': self.CanSeeApiJobCategory,
                'canSeeApiQualification': self.CanSeeApiQualification,
                'canSeeApiUser': self.CanSeeApiUser,
                'canSeeApiSection': self.CanSeeApiSection,
                'canSeeApiCompany': self.CanSeeApiCompany,
                'canSeeApiMember': self.CanSeeApiMember,
                'canSeeApiOffer': self.CanSeeApiOffer,
                'canSeeApiReview': self.CanSeeApiReview,
                # CLASSIFICATION
                'IsAAAHOSTUR': self.IsAAAHOSTUR,
                'IsMember': self.IsMember,
                'IsCompany': self.IsCompany
                }
