from dataclasses import dataclass
from . import db


@dataclass()
class Job_Category(db.Model):
    __tablename__ = "Job_Category"
    ID_JOB_CATEGORY = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(512), nullable=False)
    Description = db.Column(db.String(512), nullable=False)

    qualification = db.relationship("Qualification", backref="Job_Category", lazy=True)
