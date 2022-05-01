
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime,Date, ForeignKey,Float,Boolean
from sqlalchemy.orm import sessionmaker, relationship,backref
# from .database import Base
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine("sqlite:///auditing.db",convert_unicode=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class AuditingRequest(Base):
    __tablename__ = 'AuditingRequest'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    fileName = Column(String(100))
    state = Column(String(1000))
    public_beat = Column(String(1000))
    isValid = Column(Boolean)
    resolved = Column(Boolean,default=False)


    date = Column(DateTime,default=datetime.datetime.today())

    def __repr__(self):
        return "Request: "+self.userId


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    session.commit()
    session.close()
