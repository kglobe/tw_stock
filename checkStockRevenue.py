import datetime
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from utility import getDbUrl, getLastMonth
from log_tool import LogTool
import math
import time
from sqlalchemy.pool import NullPool
from model import check_stock_revenue

def checkStockRevenue(month):
    