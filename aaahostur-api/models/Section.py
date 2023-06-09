from dataclasses import dataclass
from .Publication_Category import Publication_Category
from . import db

@dataclass()
class Section(db.Model):
    __tablename__ = "Section"
    ID_SECTION = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Category = db.Column(db.Enum(Publication_Category))
    Description = db.Column(db.String(512), nullable=False)
    Publication_Date = db.Column(db.String(256), nullable=False)
    Schedule = db.Column(db.String(256), nullable=False)
    Img_Resource = db.Column(db.LargeBinary, nullable=True)
    Price = db.Column(db.String(128), nullable=True)
    Active = db.Column(db.Boolean, default=True)

    Id_User_Creator = db.Column(db.String(36), db.ForeignKey("User.ID_USER"))

    def to_json(self):
        return {
            "id_section": self.ID_SECTION,
            "category": self.Category,
            "description": self.Description,
            "publication_date": self.Publication_Date,
            "schedule": self.Schedule,
            "img_resource": self.Img_Resource,
            "price": self.Price,
            "active": self.Active,
            "id_user_creator": self.Id_User_Creator
        }