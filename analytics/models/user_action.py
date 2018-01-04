from analytics import Base
from sqlalchemy import Column, Integer, String

class UserAction(Base):
    __tablename__ = 'user_actions'
    id = Column(Integer, index=True, unique=True, primary_key=True)
    account = Column(String(255), index=True)
    action = Column(String(120), index=True)
    user_id = Column(Integer)
    customer_id = Column(String(64))
    web_id = Column(String(64))
    first_name = Column(String(120))
    last_name = Column(String(120))
    email = Column(String(120))
    ip_address = Column(String(255))
    referrer_url = Column(String(511))
    session = Column(String(255))
    section = Column(String(255))
    subsection = Column(String(255))
    value = Column(String(255))
    utm_source = Column(String(120))
    utm_medium = Column(String(120))
    utm_campaign = Column(String(120))
    utm_term = Column(String(120))
    utm_content = Column(String(120))
