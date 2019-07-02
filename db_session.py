from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class dbSession():
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:1111@127.0.0.1:3306/db", max_overflow=5)
        self.Session = sessionmaker(bind=self.engine)
    
    def getSession(self):
        return self.Session()

