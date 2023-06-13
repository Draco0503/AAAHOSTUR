from dataclasses import dataclass
from . import db

@dataclass()
class Member_Language(db.Model):
    __tablename__ = "Member_Language"
    ID_MEMBER_LANGUAGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Lvl = db.Column(db.String(512), nullable=False)
    Certificate = db.Column(db.LargeBinary, nullable=False)
    
    Id_Language = db.Column(db.Integer, db.ForeignKey("Language.ID_LANGUAGE"), nullable=False)
    Id_Member = db.Column(db.String(36), db.ForeignKey("Member.ID_MEMBER"), nullable=False)

    def to_json(self):
        return {'id_member_language': self.ID_MEMBER_LANGUAGE,
                'lvl': self.Lvl,
                'certificate': self.Certificate,
                'id_language': self.Id_Language,
                'id_member': self.Id_Member
                }