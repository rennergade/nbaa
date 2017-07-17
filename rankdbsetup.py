import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///datasetfull.db', echo=True)
Base = declarative_base(engine)
########################################################################
class Rankings(Base):
    """"""
    __tablename__ = 'rankings'
    __table_args__ = {'autoload':True}

#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == "__main__":
    session = loadSession()
    res = session.query(Rankings).all()
    print res[1].asset_id
