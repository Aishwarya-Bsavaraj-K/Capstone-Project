from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime,Date, ForeignKey,Float,Boolean
from sqlalchemy.orm import sessionmaker, relationship,backref
# from .database import Base
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine("sqlite:///client.db",convert_unicode=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(20))    
    password = Column(String(30))


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer,ForeignKey('users.id'))
    fileName = Column(String(100))
    beat = Column(String(400))
    date = Column(DateTime,default=datetime.datetime.today())
    is_valid = Column(Boolean,default=False)
    is_verified = Column(Boolean,default=True)
    
    user = relationship("User",backref=backref('requests'))


    def __repr__(self):
        return "Request: "+self.userId

def getData(fileName,userId=1):
    return session.query(Data).filter(Data.userId == userId and Data.fileName == fileName)

def saveRequest(userId,filename,fileHash):
    auditReqObj = AuditingRequest(userId=userId,fileName=filename,fileHash=fileHash,resolved=True,isValid=True)
    try:
        db_session.add(auditReqObj)
        db_session.commit()
        return SUCCESS
    except Exception as e:
        print(e)
        return FAILURE


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    session.commit()
    session.close()
