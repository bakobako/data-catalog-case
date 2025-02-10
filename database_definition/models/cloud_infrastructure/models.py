from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP
from models.base import Base

class PipelineRun(Base):
    __tablename__ = 'pipeline_runs'
    __table_args__ = {'schema': 'cloud_infrastructure'}

    run_id = Column(Integer, primary_key=True)
    pipeline_name = Column(String, nullable=False)
    start_timestamp = Column(TIMESTAMP, nullable=False)
    end_timestamp = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False)  # e.g., success, failed


class CloudCost(Base):
    __tablename__ = 'cloud_costs'
    __table_args__ = {'schema': 'cloud_infrastructure'}

    cost_id = Column(Integer, primary_key=True)
    cost_category = Column(String, nullable=False)  # e.g., storage, compute, network
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    cost_description = Column(Text, nullable=False)  # e.g., storage usage, API call usage
