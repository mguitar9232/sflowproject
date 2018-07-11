from kafka import KafkaConsumer

from datetime import datetime

#### aerospike import #########################
#from __future__ import print_function
import aerospike
import urllib2
import json
import sys

config = {
  'hosts': [ ('localhost', 3000) ]
}

try:
	aeroclient = aerospike.client(config).connect()
except:
#  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)
################ aerospike ##################

i = datetime.now()

key = ('flow','flow', 'flow')

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('flow', group_id='my-group', bootstrap_servers=['localhost:9092'])



for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))

    #aeroclient.put(message.key, json.loads(message.value))
    #aeroclient.put(str(i), json.loads(message.value))
    aeroclient.put(key, json.loads(message.value))
    print ("##### key=[%s] DATA=[%s]" % (message.key, message.value))

#    try:
#      #aeroclient.put(key, json.load(response))
#      aeroclient.put(message.key, json.loads(message.value))
#      print ("##### key=[%s] DATA=[%s]" % (message.key, message.value))
#    except Exception as e:
#      #import sys
#      #print ("error: {0}".format(e), file=sys.stderr)
#      #print ('error', file=sys.stderr)
#      #print >> sys.stderr, "########### error message ##############"
#      print(e.message)
#      print >> sys.stderr, "########### error message ##############"

# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

## consume json messages
#KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
#
## consume msgpack
#KafkaConsumer(value_deserializer=msgpack.unpackb)
#
## StopIteration if no message after 1sec
#KafkaConsumer(consumer_timeout_ms=1000)
#
## Subscribe to a regex topic pattern
#consumer = KafkaConsumer()
#consumer.subscribe(pattern='^awesome.*')
#
## Use multiple consumers in parallel w/ 0.9 kafka brokers
## typically you would run each on a different server / process / CPU
#consumer1 = KafkaConsumer('flow', group_id='my-group', bootstrap_servers='localhost')
#                          
##consumer2 = KafkaConsumer('flow', group_id='my-group', bootstrap_servers='localhost')
