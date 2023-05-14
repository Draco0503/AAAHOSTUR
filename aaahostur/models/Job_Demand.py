from dataclasses import dataclass
from . import db


@dataclass()
class Job_Demand(db.Model):
    __tablename__ = 'Job_Demand'
    ID_JOB_DEMAND = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Vacancies = db.Column(db.Integer, nullable=False)
    Monthly_Salary = db.Column(db.Integer)
    Contract_Type = db.Column(db.String(512))
    Schedule = db.Column(db.String(512), nullable=False)
    Working_Day = db.Column(db.String(512), nullable=False)
    Shift = db.Column(db.String(512), nullable=False)
    Holidays = db.Column(db.Integer)
    Experience = db.Column(db.String(512))
    Vehicle = db.Column(db.Boolean, default=False)
    Geographical_Mobility = db.Column(db.Boolean, default=False)
    Disability_Grade = db.Column(db.Integer, default=0)
    Others = db.Column(db.String(512))
    Id_Offer = db.Column(db.Integer, db.ForeignKey('Offer.ID_OFFER'))
