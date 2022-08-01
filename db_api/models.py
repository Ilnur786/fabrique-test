from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey
from datetime import datetime
import tzlocal
import pytz
from dataclasses import dataclass


Base = declarative_base()


@dataclass
class ModelsConfig:
	datetime_format = '%Y-%m-%d %H:%M'


class Distribution(Base, ModelsConfig):
	__tablename__ = 'distributions'

	id = Column(Integer, primary_key=True)
	# to receive time in that timezone: datetime.now(tz=pytz.timezone(tzlocal.get_localzone_name()))
	# maybe in the future it will require convert time into client tz
	# NOW it need declaration of given time format in the API docs and convert str date into datetime object (strptime)
	start_date = Column(DateTime, default=datetime.now(), comment='date when distribution will be started')
	text = Column(String, comment='message text')
	client_filter = Column(String, nullable=True,
							  comment='get some clients with filtering them by mobile operator code, tag or etc.')
	end_date = Column(DateTime, comment='date when distribution will be ended')
	was_deleted = Column(Boolean, default=False, comment='Shows if this row has been removed')
	# back_populates look to Client class "message" attribute, not to __tablename__
	message = relationship("Message", back_populates="distribution", lazy="dynamic")

	# common relationship is one-to-many. uselist=False is declarate one-to-one relate
	# back_populates declarate back direction ralative:
	# (e.g. parent-children is one-to-many, consequently, children-parent is many-to-one)

	def __repr__(self):
		return f'<Distribution: id: {self.id}, start_date: {self.start_date.strftime(self.datetime_format)}, ' \
			   f'text: "{self.text}", client_filter: "{self.client_filter}", ' \
			   f'end_date: {self.end_date.strftime(self.datetime_format)}, was_deleted: {self.was_deleted}>'


class Client(Base, ModelsConfig):
	__tablename__ = 'clients'

	id = Column(Integer, primary_key=True)
	mobile_number = Column(String(15),
							  comment='client telephone number')  # need constrainting length before added into db
	mobile_operator_code = Column(String(5),
									 comment='7XXX9354758 - three number after country code')  # need constrainting length before added into db
	tag = Column(String, comment='free fillable field. Can be nullable')
	# after API will be ready, user can give tz in "Europe/Moscow" like format.
	# Table with values are there: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
	timezone = Column(String(30), comment='it will be look like "Europe/Moscow"')
	was_deleted = Column(Boolean, default=False, comment='Shows if this row has been removed')
	# message = relationship('Association', back_populates="client")
	message = relationship('Message', back_populates="client")

	def __repr__(self):
		return f'<Client: id: {self.id}, mobile_number: "{self.mobile_number}", ' \
			   f'operator_code: "{self.mobile_operator_code}", tag: "{self.tag}", timezone: "{self.timezone}, ' \
			   f'was_deleted: {self.was_deleted}">'


class Message(Base, ModelsConfig):
	__tablename__ = 'messages'

	id = Column(Integer, primary_key=True)
	# one-to-many
	# ForeignKey look to __tablename__.attribute
	distribution_id = Column(Integer, ForeignKey('distributions.id'),
							 comment='distribution id, where message was sended')
	client_id = Column(Integer, ForeignKey('clients.id'), comment='client id whose was send message')
	distribution = relationship("Distribution", back_populates="message")
	# back_populates look to Client class "message" attribute, not to __tablename__
	client = relationship('Client', back_populates='message')
	send_date = Column(DateTime, nullable=True, default=datetime.now(),
					   comment='date when message was send. If NULL, it mean that message was not send yet')
	sending_status = Column(Boolean, default=True)

	def __repr__(self):
		return f'<Message: id: {self.id}, distribution.id: {self.distribution_id}, client.id: {self.client_id}, ' \
			   f'send_date: {self.send_date.strftime(self.datetime_format) if self.send_date else None}, ' \
			   f'sending_status: {self.sending_status}>'

# ASSOCIATION TABLE REALISATION:

####################################### 1 ####################################################
# ASSOCIATION OBJECT can be suitable if there:
# 1) Message object has composite pk (Distribution.id and Client.id), but it has own pk
# 2) Required to hold another fields in associate. table, such as date or etc.
# ON THE OTHER HAND, it required create objects through association object creation, that isn't comfortable:
	# create parent, append a child via association
	# p = Parent()
	# a = Association(extra_data="some data")
	# a.child = Child()
	# p.children.append(a)

# MANY-TO-MANY association object. Distribution and Client can relate to multiple Messages.
# DOCS HERE: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
# class Association(Base, ModelsConfig):
# 	__tablename__ = "association"
#
# 	# ForeignKey look to __tablename__.attribute
# 	client_id = Column(ForeignKey("clients.id"), primary_key=True)
# 	message_id = Column(ForeignKey("messages.id"), primary_key=True)
# 	# back_populates look to Client class "message" attribute, not to __tablename__
# 	client = relationship("Client", back_populates="messages")
# 	message = relationship("Message", back_populates="clients")


# ###################################### 2 ####################################################
# ASSOCIATION TABLE for Clients-Messages (many-to-many) relationship
# association_table = Table(
#     "association",
#     Base.metadata,
#     Column("client_id", ForeignKey("client.id"), primary_key=True),
#     Column("message_id", ForeignKey("message.id"), primary_key=True),
# )

__all__ = ["Distribution", "Client", "Message", "Base"]