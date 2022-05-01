from sqlalchemy import create_engine,func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *



SUCCESS = {'status':'success'}
FAILURE = {'status':'failure'}

engine = create_engine('sqlite:///client.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def register_user(name,email,password):
	customer = User(name=name, email=email,password=password)
	try:
		db_session.add(customer)
		db_session.commit()
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILURE

def getRequests(userId):
	return db_session.query(Data).filter(Data.userId == userId),Data

def isVerified(userId,filename):
	try:
		d = db_session.query(Data).filter(Data.userId == userId,Data.fileName == filename).one()
		if d.is_verified:
			return True
		return False

	except Exception as e:
		print(e)
		return False

def  updateStatus(userId,filename,is_valid,is_verified):
	try:
		d = db_session.query(Data).filter(Data.userId == userId,Data.fileName == filename).one()
		
		d.is_verified = is_verified
		d.is_valid = is_valid
		
		db_session.commit()
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILURE


def verify_user(email,password):
	try:
		customer = db_session.query(User).filter(User.email == email,User.password == password).one()
		return customer
	except Exception as e:
		print(e)
		return None



def save_data(user_id,filename,beat):
	data = Data(userId=user_id,fileName=filename,beat = beat)
	try:
		db_session.add(data)
		db_session.commit()
		return SUCCESS
	except Exception as e:
		print(e)
		return FAILURE



def get_data(user_id,filename):
	try:
		data = db_session.query(Data).filter(Data.userId==user_id,Data.fileName==filename).one()		
		return data
	except Exception as e:
		print(e)
		return None


