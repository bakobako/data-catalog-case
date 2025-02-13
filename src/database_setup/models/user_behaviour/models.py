from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class EmailTracking(Base):
    __tablename__ = 'email_tracking'
    __table_args__ = {'schema': 'user_behaviour'}

    email_event_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'),
                         nullable=True)  # Nullable for non-customer emails
    email_id = Column(String, nullable=False)  # Unique identifier for the email
    event_type = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    interaction_duration = Column(Float,
                                  nullable=True)  # Duration of the interaction in seconds (nullable if not applicable)
    bounce_reason = Column(Text, nullable=True)  # Reason for bounce if event_type is "bounced"

    # Relationships
    customer = relationship("Customer", backref="email_tracking")


class EmailOpenTracking(Base):
    __tablename__ = 'email_open_tracking'
    __table_args__ = {'schema': 'user_behaviour'}

    open_event_id = Column(Integer, primary_key=True)
    email_event_id = Column(Integer, ForeignKey('user_behaviour.email_tracking.email_event_id'), nullable=False)
    open_timestamp = Column(TIMESTAMP, nullable=False)
    open_duration = Column(Float, nullable=False)  # Duration the email was opened for, in seconds

    # Relationships
    email_event = relationship("EmailTracking", backref="email_open_tracking")


class WebsiteVisit(Base):
    __tablename__ = 'website_visits'
    __table_args__ = {'schema': 'user_behaviour'}

    visit_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'),
                         nullable=True)  # Nullable for anonymous visits
    session_id = Column(String, nullable=False)  # Unique session identifier
    timestamp = Column(TIMESTAMP, nullable=False)
    ip_address = Column(String, nullable=True)
    country = Column(String, nullable=True)  # Country based on IP address or geo location
    referrer_url = Column(Text, nullable=True)  # URL from which the user came (optional)

    # Relationships
    customer = relationship("Customer", backref="website_visits")


class PageView(Base):
    __tablename__ = 'page_views'
    __table_args__ = {'schema': 'user_behaviour'}

    page_view_id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey('user_behaviour.website_visits.visit_id'), nullable=False)
    page_url = Column(Text, nullable=False)  # URL of the page viewed
    page_title = Column(String, nullable=True)  # Optional title of the page
    view_duration = Column(Float, nullable=True)  # Duration of page view in seconds
    timestamp = Column(TIMESTAMP, nullable=False)

    # Relationships
    website_visit = relationship("WebsiteVisit", backref="page_views")


class BounceTracking(Base):
    __tablename__ = 'bounce_tracking'
    __table_args__ = {'schema': 'user_behaviour'}

    bounce_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'),
                         nullable=True)  # Nullable for non-customer bounces
    email_id = Column(String, nullable=False)  # Unique identifier for the email that bounced
    bounce_reason = Column(Text, nullable=False)
    bounce_timestamp = Column(TIMESTAMP, nullable=False)
    bounce_type = Column(String, nullable=False)  # e.g., "soft", "hard"

    # Relationships
    customer = relationship("Customer", backref="bounce_tracking")


class EmailClickTracking(Base):
    __tablename__ = 'email_click_tracking'
    __table_args__ = {'schema': 'user_behaviour'}

    click_event_id = Column(Integer, primary_key=True)
    email_event_id = Column(Integer, ForeignKey('user_behaviour.email_tracking.email_event_id'), nullable=False)
    click_timestamp = Column(TIMESTAMP, nullable=False)
    url_clicked = Column(Text, nullable=False)  # The URL that was clicked inside the email

    # Relationships
    email_event = relationship("EmailTracking", backref="email_click_tracking")
