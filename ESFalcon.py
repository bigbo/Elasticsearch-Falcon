#!/usr/bin/env python

__author__   ="bigbo (ljb90@live.cn)"
__date__     ="2016-08-30 14:33"
__copyright__="Copyright 2016 58, Inc"
__license__  ="58, Inc"
__version__  ="0.1"

from elasticsearch import *
import requests
import time
import json

# Global Variables
FALCON_HTTP_URL = "http://127.0.0.1:xxx/v1/push"
CLUSTER_NAME = "xxx"

# Define groups of keys
CLUSTER_NAME = "n=%s" % (CLUSTER_NAME)
SEARCH_KEYS = ['query_total', 'fetch_time_in_millis', 'fetch_total', 'fetch_time', 'query_current', 'fetch_current', 'query_time_in_millis']
GET_KEYS = ['missing_total', 'exists_total', 'current', 'time_in_millis', 'missing_time_in_millis', 'exists_time_in_millis', 'total']
DOCS_KEYS = ['count', 'deleted']
INDEXING_KEYS = ['delete_time_in_millis', 'index_total', 'index_current', 'delete_total', 'index_time_in_millis', 'delete_current']
STORE_KEYS = ['size_in_bytes', 'throttle_time_in_millis']
CACHE_KEYS = ['filter_size_in_bytes', 'field_size_in_bytes', 'field_evictions']
JVM_KEYS = ['heap_used_percent']
CLUSTER_STATUS = None
CLUSTER_STATUS_DIC = {
	'green':0,
	'red':1,
	'yellow':2
	}

CLUSTER_KEYS = SEARCH_KEYS + GET_KEYS + DOCS_KEYS + INDEXING_KEYS + STORE_KEYS

ts = int(time.time())
payload = []



def falcon_fail():
    print "FALCON_NOTSUPPORTED"
    sys.exit(2)

# Try to establish a connection to elasticsearch
try:
    conn = Elasticsearch(request_timeout=25)
except Exception, e:
    falcon_fail()


for clusterkey in CLUSTER_KEYS:
    nodestats = conn.nodes.stats()
    subtotal = 0
    cluster_data = {"endpoint":"es_cluster_data","timestamp":ts,"step":360,"counterType":"GAUGE","tags":CLUSTER_NAME}
    for nodename in nodestats[u'nodes']:
        if clusterkey in INDEXING_KEYS:
            indexstats = nodestats[u'nodes'][nodename][u'indices'][u'indexing']
        elif clusterkey in STORE_KEYS:
            indexstats = nodestats[u'nodes'][nodename][u'indices'][u'store']
        elif clusterkey in GET_KEYS:
            indexstats = nodestats[u'nodes'][nodename][u'indices'][u'get']
        elif clusterkey in DOCS_KEYS:
            indexstats = nodestats[u'nodes'][nodename][u'indices'][u'docs']
        elif clusterkey in SEARCH_KEYS:
            indexstats = nodestats[u'nodes'][nodename][u'indices'][u'search']
        try:
            subtotal += indexstats[clusterkey]
        except Exception, e:
            pass
    cluster_data["metric"] = clusterkey
    cluster_data["value"] = subtotal
    payload.append(cluster_data)

try:
    CLUSTER_STATUS = conn.cluster.health()[unicode('status')]
    CLUSTER_STATUS = CLUSTER_STATUS_DIC[CLUSTER_STATUS]
except Exception, e:
    falcon_fail()

cluster_data = {"endpoint":"es_cluster_data","timestamp":ts,"step":360,"counterType":"GAUGE","tags":CLUSTER_NAME}
cluster_data["metric"] = "cluster_status"
cluster_data["value"] = CLUSTER_STATUS
payload.append(cluster_data)

r = requests.post(FALCON_HTTP_URL, data=json.dumps(payload))

print r.text
