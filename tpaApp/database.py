from sqlalchemy import create_engine,func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
import datetime


SUCCESS = {'status':'success'}
FAILURE = {'status':'failure'}

engine = create_engine('sqlite:///auditing.db', convert_unicode=True)
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


def get_uploads():
	return restify(AuditingRequest)
	
def registerForVerification(userId,filename):
	try:
		auditReqObj = db_session.query(AuditingRequest).filter(AuditingRequest.userId == userId,AuditingRequest.fileName==filename).one()
		auditReqObj.resolved = False;
		db_session.commit()
		return SUCCESS

	except Exception as e:
		print(e)
		db_session.rollback()
		return FAILURE

def updateAuditRequest(fileName,isValid,isResolved):
	try:
		auditReqObj = db_session.query(AuditingRequest).filter(AuditingRequest.fileName == fileName).one()
		auditReqObj.resolved = isResolved;
		auditReqObj.isValid = isValid;
		db_session.commit()
		return SUCCESS

	except Exception as e:
		print(e)
		db_session.rollback()
		return FAILURE



def getHashKey(userId,filename):
	return db_session.query(AuditingRequest).filter(AuditingRequest.userId == userId,AuditingRequest.fileName==filename,AuditingRequest.resolved == False).one().fileHash

def getSize(userId,filename):
	return db_session.query(AuditingRequest).filter(AuditingRequest.userId == userId,AuditingRequest.fileName==filename,AuditingRequest.resolved == False).one().numBlocks

def getRequest(userId,auditId,filename):
	try:
		return db_session.query(AuditingRequest).filter(AuditingRequest.user_id == userId,AuditingRequest.fileName==fileName,AuditingRequest.auditId==auditId).one()
	except Exception as e:
		print(e)
		return None


def saveRequest(userId,filename):
	auditReqObj = AuditingRequest(user_id=userId,fileName=filename,resolved=False,isValid=True)
	try:
		db_session.add(auditReqObj)
		db_session.commit()
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILURE

def get_public_beat(userId,fileName):
	try:
		return db_session.query(AuditingRequest).filter(AuditingRequest.user_id == userId,AuditingRequest.fileName==fileName,AuditingRequest.resolved == False).one()
	except Exception as e:
		return ''

def getRequests():
	return db_session.query(AuditingRequest),AuditingRequest







