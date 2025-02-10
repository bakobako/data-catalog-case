from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base

class Department(Base):
    __tablename__ = 'departments'
    __table_args__ = {'schema': 'human_resources'}

    department_id = Column(Integer, primary_key=True)
    department_name = Column(String, nullable=False)
    budget = Column(DECIMAL(15, 2), nullable=True)

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'human_resources'}

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('human_resources.departments.department_id'), nullable=False)
    salary = Column(DECIMAL(15, 2), nullable=False)
    hire_date = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False)  # e.g., active, on leave, terminated

    # Relationship to the department table
    department = relationship("Department", backref="employees")
