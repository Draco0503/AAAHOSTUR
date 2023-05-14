from dataclasses import dataclass
from . import db


@dataclass()
class Member_Offer(db.Model):
    __tablename__ = "Member_Offer"
    ID_MEMBER_Offer = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Id_Offer = db.Column(db.Integer, db.ForeignKey("Offer.ID_OFFER"), nullable=False)
    Id_Member = db.Column(db.Integer, db.ForeignKey("Member.ID_MEMBER"), nullable=False)
