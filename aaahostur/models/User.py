from dataclasses import dataclass

from . import db


@dataclass()
class User(db.Model):
    __tablename__ = "User"
    ID_USER = db.Column(db.Integer, primary_key=True)
    Passwd = db.Column(db.String(512), nullable=False)
    Email = db.Column(db.String(512), unique=True, nullable=False)
    Id_Role = db.Column(db.Integer, db.ForeignKey("Role.ID_ROLE"), nullable=False)

    member = db.relationship("Member", backref="User", lazy=True)
    # member_verify = db.relationship("Member", backref="User", lazy=True)
    # member_acc_verify = db.relationship("Member", backref="User", lazy=True)

    company = db.relationship("Company", backref="User", lazy=True)
    # company_verify = db.relationship("Company", backref="User", lazy=True)

    section = db.relationship("Section", backref="User", lazy="True")
