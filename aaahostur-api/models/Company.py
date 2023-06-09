from dataclasses import dataclass
from . import db

@dataclass()
class Company(db.Model):
    __tablename__ = "Company"
    ID_COMPANY = db.Column(db.String(36), db.ForeignKey("User.ID_USER"), primary_key=True)
    Name = db.Column(db.String(512), nullable=False)
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
    
    Id_Company_Parent = db.Column(db.String(36), db.ForeignKey("Company.ID_COMPANY"), nullable=True)
    Id_User_Verify = db.Column(db.String(36), db.ForeignKey("User.ID_USER"), nullable=True)

    company_account = db.relationship("Company_Account", backref="Company", lazy=True)

    def to_json(self):
        return {'id_company': self.ID_COMPANY,
                "name": self.Name,
                'type': self.Type,
                'cif': self.CIF,
                'address': self.Address,
                'cp': self.CP,
                'city': self.City,
                'province': self.Province,
                'contact_name': self.Contact_Name,
                'contact_phone': self.Contact_Phone,
                'contact_email': self.Contact_Email,
                'description': self.Description,
                'verify': self.Verify,
                'active': self.Active,
                'id_company_parent': self.Id_Company_Parent,
                'Id_User_Verify': self.Id_User_Verify
                }