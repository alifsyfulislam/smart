import datetime
import urllib
import urllib.parse, random, string, requests
import io
from gluon.contenttype import contenttype
from openpyxl import Workbook
import re

# =================== Server Time =========================
# date_fixed=datetime.datetime.now()+datetime.timedelta(hours=6)
date_fixed=datetime.datetime.now()
present_date = date_fixed.strftime('%Y-%m-%d')
present_datetime = date_fixed.strftime('%Y-%m-%d %H:%M:%S')
# =================== Server Time =========================

# =================== Secondary ===========================
db = DAL('mysql://smart:dddsdfiewrklwsfio28332ojewidnzZz@34.142.146.190/smart', decode_credentials=True)
# =================== Secondary ===========================

# =================== Primary ===========================
db2 = DAL('mysql://tcpl_secondary:dddsec9xyz123@35.197.145.58/tcpl', decode_credentials=True)
# =================== Primary ===========================



