from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP, Float, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class RegionalDemographics(Base):
    __tablename__ = 'regional_demographics'
    __table_args__ = {'schema': 'czech_market_data'}

    region_id = Column(Integer, primary_key=True)
    region_name = Column(String, nullable=False)
    district_name = Column(String, nullable=True)  # For more granular data
    population = Column(Integer, nullable=False)
    avg_age = Column(Float, nullable=False)
    unemployment_rate = Column(Float, nullable=False)
    avg_salary = Column(DECIMAL(10, 2), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)  # When this data was recorded
    households_count = Column(Integer, nullable=False)
    population_density = Column(Float, nullable=False)  # people per km2

class PropertyMarketStats(Base):
    __tablename__ = 'property_market_stats'
    __table_args__ = {'schema': 'czech_market_data'}

    stat_id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('czech_market_data.regional_demographics.region_id'), nullable=False)
    property_type = Column(String, nullable=False)  # apartment, house, land
    avg_price_per_m2 = Column(DECIMAL(10, 2), nullable=False)
    avg_rental_price_per_m2 = Column(DECIMAL(10, 2), nullable=True)
    number_of_transactions = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    year_over_year_price_change = Column(Float, nullable=False)  # percentage

    region = relationship("RegionalDemographics", backref="market_stats")

class NewDevelopmentProject(Base):
    __tablename__ = 'new_development_projects'
    __table_args__ = {'schema': 'czech_market_data'}

    project_id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('czech_market_data.regional_demographics.region_id'), nullable=False)
    project_name = Column(String, nullable=False)
    developer_name = Column(String, nullable=False)
    total_units = Column(Integer, nullable=False)
    available_units = Column(Integer, nullable=False)
    completion_date = Column(TIMESTAMP, nullable=True)
    price_range_min = Column(DECIMAL(15, 2), nullable=False)
    price_range_max = Column(DECIMAL(15, 2), nullable=False)
    project_status = Column(String, nullable=False)  # planning, under construction, completed
    has_parking = Column(Boolean, nullable=False)
    website_url = Column(String, nullable=True)

    region = relationship("RegionalDemographics", backref="development_projects")

class MortgageStats(Base):
    __tablename__ = 'mortgage_stats'
    __table_args__ = {'schema': 'czech_market_data'}

    stat_id = Column(Integer, primary_key=True)
    bank_name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    min_down_payment_percentage = Column(Float, nullable=False)
    max_ltv = Column(Float, nullable=False)  # Loan to Value ratio
    timestamp = Column(TIMESTAMP, nullable=False)
    fixation_period_years = Column(Integer, nullable=False) 