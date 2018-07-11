# import the module
from __future__ import print_function
import aerospike
import urllib2
import json

config = {
  'hosts': [ ('localhost', 3000) ]
}

try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

key = ('ip', 'hit', 'trial')

try:
  for i in range(0,255):
    for j in range(0,255):
        for k in range(0,255):
            for l in range(0,255):
                if not((i == 198 and j == 168) or (i == 172 and j > 15 and j < 32) or (i == 10)):
                    response = urllib2.urlopen('http://ip-api.com/json/'+str(i)+'.'+str(j)+'.'+str(k)+'.'+str(l))
                    #html = response.read()
                    client.put(key, json.load(response))
except Exception as e:
  import sys
  print("error: {0}".format(e), file=sys.stderr)


client.close()
