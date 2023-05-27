from dataclasses import dataclass
from . import db

@dataclass()
class Job_Demand_Language(db.Model):
    __tablename__ = "Job_Demand_Language"
    ID_JOB_DEMAND_LANGUAGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    Id_Language = db.Column(db.Integer, db.ForeignKey("Language.ID_LANGUAGE"), nullable=False)
    Id_Job_Demand = db.Column(db.Integer, db.ForeignKey("Job_Demand.ID_JOB_DEMAND"), nullable=False)
    
    def to_json(self):
        return {'id_job_demand_language': self.ID_JOB_DEMAND_LANGUAGE,
                'id_language': self.Id_Language,
                'id_job_demand': self.Id_Job_Demand
                }