from dataclasses import dataclass
from . import db


@dataclass()
class Job_Demand_Category(db.Model):
    __tablename__ = "Job_Demand_Category"
    ID_JOB_DEMAND_CATEGORY = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Id_Job_Category = db.Column(db.Integer, db.ForeignKey("Job_Category.ID_JOB_CATEGORY"), nullable=False)
    Id_Job_Demand = db.Column(db.Integer, db.ForeignKey("Job_Demand.ID_JOB_DEMAND"), nullable=False)
