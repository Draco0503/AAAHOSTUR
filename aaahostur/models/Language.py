from dataclasses import dataclass
from . import db


@dataclass()
class Language(db.Model):
    __tablename__ = "Language"
    ID_LANGUAGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(512), nullable=False)
    Lvl = db.Column(db.String(512), nullable=False)
    Certificate = db.Column(db.String(512), nullable=False)

    def to_json(self):
        return {'id_language': self.ID_LANGUAGE,
                'name': self.Name,
                'Lv1': self.Lvl,
                'certificate': self.Certificate
                }
