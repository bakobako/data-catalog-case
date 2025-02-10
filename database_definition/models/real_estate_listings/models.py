from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base


class RawRealEstateListing(Base):
    __tablename__ = 'raw_real_estate_listings'
    __table_args__ = {'schema': 'real_estate_listings'}

    listing_id = Column(Integer, primary_key=True)
    source_portal = Column(Text, nullable=False)
    listing_url = Column(Text, nullable=False)
    short_description = Column(Text, nullable=False)
    long_description = Column(Text, nullable=False)
    ingested_at = Column(TIMESTAMP, nullable=False)


class Location(Base):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'real_estate_listings'}

    location_id = Column(Text, primary_key=True)
    city = Column(Text, nullable=False)
    district = Column(Text, nullable=True)
    street = Column(Text, nullable=True)
    house_number = Column(Text, nullable=True)
    latitude = Column(DECIMAL(9, 6), nullable=True)
    longitude = Column(DECIMAL(9, 6), nullable=True)


class AnalysedRealEstateListing(Base):
    __tablename__ = 'analysed_real_estate_listings'
    __table_args__ = {'schema': 'real_estate_listings'}

    listing_id = Column(Integer, ForeignKey('real_estate_listings.raw_real_estate_listings.listing_id'),
                        primary_key=True)
    property_type = Column(Text, nullable=False)
    listing_price = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(Text, nullable=False)
    location_id = Column(Text, ForeignKey('real_estate_listings.locations.location_id'), nullable=False)
    listing_status = Column(Text, nullable=True)
    num_bedrooms = Column(Integer, nullable=True)
    num_bathrooms = Column(Integer, nullable=True)
    area_m2 = Column(DECIMAL(10, 2), nullable=True)
    apartment_layout = Column(Text, nullable=True)
    is_walkthrough_apartment = Column(Boolean, nullable=True)
    floor_number = Column(Integer, nullable=True)
    building_floors = Column(Integer, nullable=True)
    type_of_ownership = Column(Text, nullable=True)
    type_of_building = Column(Text, nullable=True)
    condition = Column(Text, nullable=True)
    energy_efficiency_label = Column(Text, nullable=True)
    energy_usage = Column(DECIMAL(10, 2), nullable=True)
    monthly_payments_czk = Column(DECIMAL(15, 2), nullable=True)
    is_rooftop_apartment = Column(Boolean, nullable=True)
    is_mezonet = Column(Boolean, nullable=True)
    has_balcony = Column(Boolean, nullable=True)
    balcony_area_m2 = Column(DECIMAL(10, 2), nullable=True)
    has_terrace = Column(Boolean, nullable=True)
    terrace_area_m2 = Column(DECIMAL(10, 2), nullable=True)
    has_parking_spot = Column(Boolean, nullable=True)
    has_garage = Column(Boolean, nullable=True)
    has_elevator = Column(Boolean, nullable=True)
    has_cellar = Column(Boolean, nullable=True)
    cellar_area_m2 = Column(DECIMAL(10, 2), nullable=True)
    flooring_type = Column(Text, nullable=True)

    raw_listing = relationship("RawRealEstateListing", backref="analysed_listing", uselist=False)
    location = relationship("Location", backref="analysed_listing")


class ListingPhoto(Base):
    __tablename__ = 'listing_photos'
    __table_args__ = {'schema': 'real_estate_listings'}

    photo_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('real_estate_listings.analysed_real_estate_listings.listing_id'),
                        nullable=False)
    photo_url = Column(Text, nullable=False)
    photo_type = Column(Text, nullable=False)
    upload_timestamp = Column(TIMESTAMP, nullable=False)

    analysed_listing = relationship("AnalysedRealEstateListing", backref="listing_photos")
