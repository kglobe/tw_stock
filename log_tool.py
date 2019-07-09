# -*- coding: utf-8 -*-
"""
Created on 2019/03/06

@author: I26436
"""
import os
import datetime
import time
import logging
from model import error_log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utility import getDbUrl

class LogTool:

    def __init__(self,pyFile,errorType):
        self.pyFile = pyFile
        self.errorType = errorType
    
    def log_dataBase(self,msg):
        try:
            self.log_txt(msg)
                    
            engine = create_engine(getDbUrl())
            DB_Session = sessionmaker(bind=engine)
            session = DB_Session()

            updatedate = datetime.datetime.now().strftime('%Y%m%d')
            updatetime = datetime.datetime.now().strftime('%H%M%S')

            errorLog = error_log()
            errorLog.priKey = str(int(round(time.time() * 100000)))
            errorLog.pyFile = self.pyFile
            errorLog.errorType = self.errorType
            errorLog.msg = msg
            errorLog.updateDate = updatedate
            errorLog.updateTime = updatetime
            session.add(errorLog)
            session.commit()
        except Exception as e:
            try:
                self.log_txt(" log_dataBase Exception: "+str(e))
            except Exception as e:
                print(str(e))
        finally:
            try:
                session.close()
            except Exception as e:
                return
    
    def log_txt(self,msg):
        try:
            if not os.path.exists('/python_log/'):
                os.makedirs('/python_log/')
            errlogger = self.setup_logger('/python_log/'+self.pyFile+'.log')
            errlogger.error(msg)
        except Exception as e:
            print(str(e))

    def setup_logger(self,log_file,level=logging.ERROR):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        logger = logging.getLogger(self.pyFile)
        logger.setLevel(level)
        if len(logger.handlers) == 0:
            logger.addHandler(handler)
        
        return logger
