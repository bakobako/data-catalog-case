from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base

class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'sales'}

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True)
    signup_date = Column(TIMESTAMP, nullable=False)
    status = Column(String, nullable=False)  # e.g., active, canceled, trial
    preferred_contact_method = Column(String, nullable=True)  # e.g., email, phone

    # Relationships
    transactions = relationship('Transaction', backref='customer', lazy='dynamic')
    subscriptions = relationship('Subscription', backref='customer', lazy='dynamic')


class Transaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'sales'}

    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'), nullable=False)
    transaction_type = Column(String, nullable=False)  # e.g., purchase, subscription, refund
    amount = Column(DECIMAL(15, 2), nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(TIMESTAMP, nullable=False)
    payment_method = Column(String, nullable=True)  # e.g., credit card, PayPal

    # Relationship to customer
    customer = relationship('Customer', backref='transactions')


class Subscription(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = {'schema': 'sales'}

    subscription_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'), nullable=False)
    subscription_plan = Column(String, nullable=False)  # e.g., basic, premium
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=True)
    status = Column(String, nullable=False)  # e.g., active, canceled, expired

    # Relationship to customer
    customer = relationship('Customer', backref='subscriptions')
