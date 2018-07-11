#-*-coding:utf-8
#########################################################################################################
#  name : ripe_api.py
#  desc : ripe open api search as number[for global as number]
#       :
#--------------------------------------------------------------------------------------------------------
#  open api url :
#   url = "http://stat.ripe.net/data/abuse-contact-finder/data.json?resource=[AS NUMBER]"
#########################################################################################################

from time import sleep

import sys
import urllib
import json
import datetime

import pymysql

reload(sys)
sys.setdefaultencoding('utf-8')

as_number=0

arg_option=0

argc = len(sys.argv)
if(argc >=1):
  if(argc ==1):
    print("All update")
    arg_option = 0
  elif(argc ==2):
    arg_option = 1
    as_number = sys.argv[1]
  else:
    print('[Error]Argument count is wrong. \n')
    exit(1)
else:
  print('[Error]Argument is not enough. \n')
  exit(1)

# MYSQL CONNECTION
conn = pymysql.connect(host='127.0.0.1', user='testuser', password='password', db='pmacct', charset='utf8')

curs = conn.cursor(pymysql.cursors.DictCursor)

if(arg_option==0):
 
 # ==== select example ====
 sql = "select as_dst from pmacct.acct_dstas_info where as_eng_name is null"
 curs.execute(sql)
 
 # DATA Fetch
 rows = curs.fetchall()
 
 for row in rows:
   as_number=row['as_dst']
   print row['as_dst'] 
   print as_number
 
 ############ URL CALL & JSON PARSING
   url3 = "http://stat.ripe.net/data/abuse-contact-finder/data.json?resource={0}".format(as_number)
 
   print url3
 
   urlcall = urllib.urlopen(url3)
 
   data = urlcall.read()
 
   print data
 
   jdata = json.loads(data)
 
 
   try:
    engname = jdata["data"]["holder_info"]["name"]
 
   except Exception, e:
    print "############## CONTINUE 1 ################"
    continue
 
   try:
    usql2 = "UPDATE pmacct.acct_dstas_info SET as_eng_name= '{0}' WHERE as_dst = '{1}'".format(engname, as_number)
    curs.execute(usql2)
 
    print "engname:"+ engname
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## CONTINUE 2 ################"
    continue
 
   conn.commit()
 
   sleep(1)

elif(arg_option==1):
 ############ URL CALL & JSON PARSING
   url3 = "http://stat.ripe.net/data/abuse-contact-finder/data.json?resource={0}".format(as_number)
 
   print url3
 
   urlcall = urllib.urlopen(url3)
 
   data = urlcall.read()
 
   print data
 
   jdata = json.loads(data)
 
   try:
    engname = jdata["data"]["holder_info"]["name"]
 
   except Exception, e:
    print "############## EXCEPTION 1 ################"
 
   try:
    usql2 = "UPDATE pmacct.acct_dstas_info SET as_eng_name= '{0}' WHERE as_dst = '{1}'".format(engname, as_number)
    curs.execute(usql2)
 
    print "engname:"+ engname
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## EXCEPTION 2 ################"
 
   conn.commit()


else:
  print('NO ARGUMENT')
  conn.close()
  exit(1)

conn.close()
