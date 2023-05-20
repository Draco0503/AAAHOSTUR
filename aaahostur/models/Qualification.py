from dataclasses import dataclass

from . import db


@dataclass()
class Qualification(db.Model):
    __tablename__ = "Qualification"
    ID_QUALIFICATION = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(512), nullable=False)
    Description = db.Column(db.String(512), nullable=False)

    Id_Qualification_Parent = db.Column(db.Integer, db.ForeignKey("Qualification.ID_QUALIFICATION"), nullable=True)
    Id_Job_Category = db.Column(db.Integer, db.ForeignKey("Job_Category.ID_JOB_CATEGORY"), nullable=True)

    def to_json(self):
        return {
            "id_qualification": self.ID_QUALIFICATION,
            "name": self.Name,
            "description": self.Description
        }
