from dataclasses import dataclass
import datetime as dt

from . import db


@dataclass()
class Member(db.Model):
    __tablename__ = "Member"
    ID_MEMBER = db.Column(db.Integer, db.ForeignKey("User.ID_USER"), primary_key=True)
    Name = db.Column(db.String(512), nullable=False)
    Surname = db.Column(db.String(512), nullable=False)
    DNI = db.Column(db.String(512), nullable=False, unique=True)
    Address = db.Column(db.String(512), nullable=False)
    CP = db.Column(db.String(512), nullable=False)
    City = db.Column(db.String(512), nullable=False)
    Province = db.Column(db.String(512), nullable=False)
    PNA_Address = db.Column(db.String(512), nullable=True)
    PNA_CP = db.Column(db.String(512), nullable=True)
    PNA_City = db.Column(db.String(512), nullable=True)
    PNA_Province = db.Column(db.String(512), nullable=True)
    Gender = db.Column(db.String(1), nullable=False)
    Land_Line = db.Column(db.String(512), nullable=True)
    Mobile = db.Column(db.String(512), nullable=False)
    Profile_Picture = db.Column(db.LargeBinary, nullable=True)
    Birth_Date = db.Column(db.String(256), nullable=False)
    Vehicle = db.Column(db.Boolean, default=False)
    Geographical_Mobility = db.Column(db.Boolean, default=False)
    Disability_Grade = db.Column(db.Integer, default=0)
    Join_Date = db.Column(db.String(256), default=dt.datetime.now(), nullable=False)
    Active = db.Column(db.Boolean, default=True)
    Cancelation_Date = db.Column(db.String(256), nullable=True)
    Verify = db.Column(db.Boolean, default=False)

    Id_User_Verify = db.Column(db.Integer, db.ForeignKey("User.ID_USER"))

    member_account = db.relationship("Member_Account", backref="Member", lazy=True)
    member_language = db.relationship("Member_Language", backref="Member", lazy=True)
    academic_profile = db.relationship("Academic_Profile", backref="Member", lazy=True)

    def to_json(self):
        return {'id_member': self.ID_MEMBER,
                'name': self.Name,
                'surname': self.Surname,
                'dni': self.DNI,
                'adderss': self.Address,
                'cp': self.CP,
                'city': self.City,
                'province': self.Province,
                'pna_address': self.PNA_Address,
                'pna_cp': self.PNA_CP,
                'pna_city': self.PNA_City,
                'pna_province': self.PNA_Province,
                'gender': self.Gender,
                'land_line': self.Land_Line,
                'mobile': self.Mobile,
                'profile_picture': self.Profile_Picture,
                'birth_date': self.Birth_Date,
                'vehicle': self.Vehicle,
                'geographical_mobility': self.Geographical_Mobility,
                'disability_grade': self.Disability_Grade,
                'join_date': self.Join_Date,
                'active': self.Active,
                'cancelation_date': self.Cancelation_Date,
                'verify': self.Verify,
                'id_user_verify': self.Id_User_Verify
                }