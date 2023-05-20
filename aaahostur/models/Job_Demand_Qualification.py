from dataclasses import dataclass
from . import db


@dataclass()
class Job_Demand_Qualification(db.Model):
    __tablename__ = "Job_Demand_Qualification"
    ID_JOB_DEMAND_QUALIFICATION = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Id_Qualification = db.Column(db.Integer, db.ForeignKey("Qualification.ID_QUALIFICATION"), nullable=False)
    Id_Job_Demand = db.Column(db.Integer, db.ForeignKey("Job_Demand.ID_JOB_DEMAND"), nullable=False)

    def to_json(self):
        return {'id_job_demand_qualification': self.ID_JOB_DEMAND_QUALIFICATION,
                'id_qualification': self.Id_Qualification,
                'id_job_demand': self.Id_Job_Demand
                }