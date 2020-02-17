
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
import configparser as cfgp

config = cfgp.ConfigParser()
config.read('config.ini')
default = config['DEFAULT']

Base = declarative_base()
#engine = create_engine('sqlite:///:memory:')
#engine = create_engine('sqlite:///sandbox-db.sqlite')
engine = create_engine(default['SqlLite'])
Session = sessionmaker(bind=engine)
session = Session()

# objects
class Record(Base):
    __tablename__ = 'record'

    def __repr__ (self):
        return "<Record(id='%s')>" % (self.id)

    id = Column(Integer, Sequence('rec_id_seq'), primary_key=True)
    account = Column(String(255))
    url = Column(String(255))
    notes = Column(Text)
    tag = Column(String(255))
    subrecords = relationship("SubRecord", backref="record")
    files = relationship("File", backref="record")

class SubRecord(Base):
    __tablename__ = 'subrecord'

    def __repr__(self):
        return "<SubRecord(id='%s')>" % (self.id)

    id = Column(Integer, Sequence('subr_id_seq'), primary_key=True)
    rec_id = Column(Integer, ForeignKey('record.id'))
    user = Column(String(255))
    password = Column(Text)

class File(Base):
    __tablename__ = 'file'

    def __repr__(self):
        return "<File(id='%s')>" % (self.id)

    id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    rec_id = Column(Integer, ForeignKey('record.id'))
    filename = Column(String(255))
    path = Column(String(255))


Base.metadata.create_all(engine)

# Record CRUD
def addRecord(record):
    try:
        session.add(record)
        session.commit()
        return record.id
    except:
        session.rollback()
    finally:
        session.close()


def updateRecord(rec_id, update_record):
    try:
        record = session.query(Record).filter(Record.id == rec_id).first()
        record.account = update_record.account
        record.url = update_record.url
        record.notes = update_record.notes
        record.tag = update_record.tag
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def delRecord(rec_id):
    try:
        record = session.query(Record).filter(Record.id == rec_id).first()
        session.delete(record)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def getByRecordId(rec_id):
    return session.query(Record).filter(Record.id == rec_id).first()

def queryAllRecord():
    results = session.query(Record).all()
    return results

# criteria, Record.id == 1
def searchRecord(criteria):
    results = session.query(Record).filter(criteria).all()
    return results

## query(Rec).order_by(Rec.prop)
## query(Rec).order_by(desc(Rec.prop))

# SubRecord CRUD
def appendSubRecord(rec_id, subrecord):
    try:
        record = session.query(Record).filter(Record.id == rec_id).first()
        record.subrecords.append(subrecord)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def delSubRecord(rec_id):
    try:
        record = session.query(SubRecord).filter(SubRecord.id == rec_id).first()
        session.delete(record)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def queryAllSubRecord():
    results = session.query(SubRecord).all()
    return results

def getRecentSubRecord(rec_id):
    record = session.query(SubRecord).filter(SubRecord.rec_id == rec_id).order_by(desc(SubRecord.id)).first()
    return record

def searchSubRecord(criteria):
    results = session.query(SubRecord).filter(criteria).all()
    return results


# File CRUD
def appendFile(rec_id, newfile):
    try:
        record = session.query(Record).filter(Record.id == rec_id).first()
        record.files.append(newfile)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def delFile(rec_id):
    try:
        record = session.query(File).filter(File.id == rec_id).first()
        session.delete(record)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def queryAllFile():
    results = session.query(File).all()
    return results

