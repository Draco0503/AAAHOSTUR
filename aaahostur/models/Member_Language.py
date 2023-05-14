from dataclasses import dataclass
from . import db


@dataclass()
class Member_Language(db.Model):
    __tablename__ = "Member_Language"
    ID_MEMBER_LANGUAGE = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Id_Language = db.Column(db.Integer, db.ForeignKey("Language.ID_LANGUAGE"), nullable=False)
    Id_Member = db.Column(db.Integer, db.ForeignKey("Member.ID_MEMBER"), nullable=False)