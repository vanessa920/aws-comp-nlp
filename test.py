from engine import engine, testinit,loadEngine,saveEngine
from datetime import datetime
import os
from utilities import *

test_engine = engine()
test_engine.loadCSV('city_SanJose_Minutes.csv')

filename = 'test_engine'

saveEngine(filename,test_engine)
