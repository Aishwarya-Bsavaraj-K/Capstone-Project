from sqlalchemy import create_engine,func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
import datetime


SUCCESS = {'status':'success'}
FAILURE = {'status':'failure'}

engine = create_engine('sqlite:///cloud.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def restify(queryObj):
	values = []
	for row in db_session.query(queryObj):
		temp = {}
		for column in queryObj.__table__.columns.keys():
			temp[column] = getattr(row,column)
		values.append(temp)

	# print(values)
	return {'values':values}



def save_file(userId,filename,tag,state,public_beat):
	auditReqObj = Data(userId=userId,fileName=filename,tag=tag,state=state,public_beat=public_beat)
	try:
		db_session.add(auditReqObj)
		db_session.commit()
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILURE

def get_data(userId,fileName):
	try:
		return db_session.query(Data).filter(Data.userId == userId,Data.fileName == fileName).one()
	except Exception as e:
		print(e)
		return ''

def get_uploads():
	return restify(Data)






