from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = {'schema': 'customer_support'}

    ticket_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('sales.customers.customer_id'), nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Text, default="open", nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    assigned_to_employee_id = Column(Integer, ForeignKey('human_resources.employees.employee_id'), nullable=True)

    # Relationships
    customer = relationship("Customer", backref="tickets")
    assigned_to_employee = relationship("Employee", backref="assigned_tickets", uselist=False)
    conversations = relationship("Conversation", backref="ticket", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = 'conversations'
    __table_args__ = {'schema': 'customer_support'}

    conversation_id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('customer_support.tickets.ticket_id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('human_resources.employees.employee_id'),
                         nullable=True)  # Nullable for customer-originated conversations
    started_at = Column(TIMESTAMP, nullable=False)
    ended_at = Column(TIMESTAMP, nullable=True)  # Null if ongoing

    # Relationships
    employee = relationship("Employee", backref="conversations", uselist=False)
    messages = relationship("Message", backref="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'schema': 'customer_support'}

    message_id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('customer_support.conversations.conversation_id'), nullable=False)
    sender_type = Column(Text, nullable=False)  # Defines if the message is from a customer or support agent
    message_text = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    # Relationship
    conversation = relationship("Conversation", backref="messages")


class TicketHistory(Base):
    __tablename__ = 'ticket_history'
    __table_args__ = {'schema': 'customer_support'}

    history_id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('customer_support.tickets.ticket_id'), nullable=False)
    status_changed_to = Column(Text, nullable=False)
    changed_by_employee_id = Column(Integer, ForeignKey('human_resources.employees.employee_id'), nullable=False)
    changed_at = Column(TIMESTAMP, nullable=False)

    # Relationships
    ticket = relationship("Ticket", backref="ticket_history")
    changed_by_employee = relationship("Employee", backref="ticket_history")
