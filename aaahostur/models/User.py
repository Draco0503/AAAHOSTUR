from dataclasses import dataclass
from . import db
import uuid


@dataclass()
class User(db.Model):
    __tablename__ = "User"
    ID_USER = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
    Passwd = db.Column(db.String(512), nullable=False)
    Email = db.Column(db.String(512), unique=True, nullable=False)

    Id_Role = db.Column(db.Integer, db.ForeignKey("Role.ID_ROLE"), nullable=False)

    member = db.relationship("Member", backref="User", lazy=True, foreign_keys="[Member.ID_MEMBER]")
    # member_verify = db.relationship("Member", backref="User", lazy=True)
    # member_acc_verify = db.relationship("Member", backref="User", lazy=True)

    company = db.relationship("Company", backref="User", lazy=True, foreign_keys="[Company.ID_COMPANY]")
    # company_verify = db.relationship("Company", backref="User", lazy=True)

    section = db.relationship("Section", backref="User", lazy=True, foreign_keys="[Section.Id_User_Creator]")

    def to_json(self):
        return {
            "id_user": self.ID_USER,
            "email": self.Email,
            "id_role": self.Id_Role
        }
