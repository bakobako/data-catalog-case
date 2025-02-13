from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP, Float, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class TransportStop(Base):
    __tablename__ = 'transport_stops'
    __table_args__ = {'schema': 'location_amenities'}

    stop_id = Column(Integer, primary_key=True)
    stop_name = Column(String, nullable=False)
    transport_type = Column(String, nullable=False)  # metro, tram, bus, train
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    zone = Column(String, nullable=True)  # transport zone
    wheelchair_accessible = Column(Boolean, nullable=False)
    lines = Column(String, nullable=False)  # Comma-separated list of lines serving this stop

class School(Base):
    __tablename__ = 'schools'
    __table_args__ = {'schema': 'location_amenities'}

    school_id = Column(Integer, primary_key=True)
    school_name = Column(String, nullable=False)
    school_type = Column(String, nullable=False)  # kindergarten, primary, secondary, university
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    website = Column(String, nullable=True)
    language_of_instruction = Column(String, nullable=False)  # Czech, English, etc.
    is_private = Column(Boolean, nullable=False)

class PointOfInterest(Base):
    __tablename__ = 'points_of_interest'
    __table_args__ = {'schema': 'location_amenities'}

    poi_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # restaurant, grocery, shopping_mall, hospital, etc.
    subcategory = Column(String, nullable=True)  # e.g., for restaurants: czech, italian, etc.
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    opening_hours = Column(String, nullable=True)  # JSON string of opening hours
    website = Column(String, nullable=True)
    phone = Column(String, nullable=True)

class HealthcareFacility(Base):
    __tablename__ = 'healthcare_facilities'
    __table_args__ = {'schema': 'location_amenities'}

    facility_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)  # hospital, clinic, pharmacy, etc.
    specialization = Column(String, nullable=True)  # For clinics/hospitals
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    emergency_service = Column(Boolean, nullable=False)
    phone = Column(String, nullable=False)
    website = Column(String, nullable=True)

class ParkingZone(Base):
    __tablename__ = 'parking_zones'
    __table_args__ = {'schema': 'location_amenities'}

    zone_id = Column(Integer, primary_key=True)
    zone_type = Column(String, nullable=False)  # blue, purple, orange, etc.
    district = Column(String, nullable=False)
    price_per_hour = Column(DECIMAL(10, 2), nullable=True)
    resident_permit_price = Column(DECIMAL(10, 2), nullable=True)
    geometry = Column(String, nullable=False)  # GeoJSON of zone boundaries
    restrictions = Column(String, nullable=True)  # Any special restrictions or rules 