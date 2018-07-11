#-*-coding:utf-8
#########################################################################################################
#  name : whois_api.py
#  desc : whois open api search as number
#       :
#--------------------------------------------------------------------------------------------------------
#  open api url : 
#   url1 = "http://whois.kisa.or.kr/openapi/whois.jsp?query=AS[AS NUMBER]&key=xxxxxxxxxxxxxxxxxxxxxx&answer=json"
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
 sql = "SELECT as_dst FROM pmacct.acct_dstas_info"
 curs.execute(sql)
 
 # DATA Fetch
 rows = curs.fetchall()
 
 for row in rows:
   as_number=row['as_dst']
   print row['as_dst'] 
   print as_number
 
 ############ URL CALL & JSON PARSING
   url1 = "http://whois.kisa.or.kr/openapi/whois.jsp?query=AS"
   url2 = "&key=xxxxxxxxxxxxxxxxxxxxxxxxxxx&answer=json".format(as_number)
   url3 = "{0}{1}{2}".format(url1,as_number,url2)
 
   print url3
 
   urlcall = urllib.urlopen(url3)
 
   data = urlcall.read()
 
   print data
 
   jdata = json.loads(data)
 
 
   countrycode = jdata["whois"]["countryCode"]
 
 #  print "countrycode:"
 #
 #  print countrycode
 
   try:
     usql = "UPDATE pmacct.acct_dstas_info SET country_code='{0}' WHERE as_dst = '{1}'".format(countrycode, as_number)
     curs.execute(usql)
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## PYMYSQL ERROR ################"
 
   conn.commit()
 #  prin "\n"
 
   try:
    engname = jdata["whois"]["english"]["asName"]
 
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
 #        if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
 #            handle_duplicate_pymysql_exception(e, func_a)
 #        else:
 #            raise
   except Exception as e:
    print "############## CONTINUE 3 : UNKNOWN ERROR ################"
    continue
 
   conn.commit()
   print "\n"
 
   try:
    orgname = jdata["whois"]["english"]["orgInfo"]["name"]
 
    print "orgname:" + orgname
   except Exception, e:
    orgname = jdata["whois"]["korean"]["orgInfo"]["name"]
 
    print "######### orgname:" + orgname
 
   try:
    usql3 = "UPDATE pmacct.acct_dstas_info SET as_org_name= '{0}' WHERE as_dst = '{1}'".format(orgname, as_number)
    curs.execute(usql3)
 
    print "engname:"+ engname
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## CONTINUE 2 ################"
    continue
 
   conn.commit()
 
   sleep(1)

elif(arg_option==1):
 ############ URL CALL & JSON PARSING
   url1 = "http://whois.kisa.or.kr/openapi/whois.jsp?query=AS"
   url2 = "&key=xxxxxxxxxxxxxxxxxxxxxxxxxxx&answer=json".format(as_number)
   url3 = "{0}{1}{2}".format(url1,as_number,url2)
 
   print url3
 
   urlcall = urllib.urlopen(url3)
 
   data = urlcall.read()
 
   print data
 
   jdata = json.loads(data)
 
 
   countrycode = jdata["whois"]["countryCode"]
 
 #  print "countrycode:"
 #
 #  print countrycode
 
   try:
     usql = "UPDATE pmacct.acct_dstas_info SET country_code='{0}' WHERE as_dst = '{1}'".format(countrycode, as_number)
     curs.execute(usql)
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## PYMYSQL ERROR ################"
 
   conn.commit()
 #  prin "\n"
 
   try:
    engname = jdata["whois"]["english"]["asName"]
 
   except Exception, e:
    print "############## EXCEPTION 1 ################"
 
   try:
    usql2 = "UPDATE pmacct.acct_dstas_info SET as_eng_name= '{0}' WHERE as_dst = '{1}'".format(engname, as_number)
    curs.execute(usql2)
 
    print "engname:"+ engname
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## EXCEPTION 2 ################"
 #        if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
 #            handle_duplicate_pymysql_exception(e, func_a)
 #        else:
 #            raise
   except Exception as e:
    print "############## CONTINUE 3 : UNKNOWN ERROR ################"
    print "############## EXCEPTION 3 ################"
 
   conn.commit()
   print "\n"
 
   try:
    orgname = jdata["whois"]["english"]["orgInfo"]["name"]
 
    print "orgname:" + orgname
   except Exception, e:
    orgname = jdata["whois"]["korean"]["orgInfo"]["name"]
 
    print "######### orgname:" + orgname
 
   try:
    usql3 = "UPDATE pmacct.acct_dstas_info SET as_org_name= '{0}' WHERE as_dst = '{1}'".format(orgname, as_number)
    curs.execute(usql3)
 
    print "engname:"+ engname
 
   except pymysql.Error as e:
    print e.message or e.args
    print "############## EXCEPTION 4 ################"
 
   conn.commit()

else:
  print('NO ARGUMENT')
  conn.close()
  exit(1)

conn.close()
