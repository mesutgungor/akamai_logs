#!/usr/bin/python
import requests
import urllib.parse
import json
import gzip
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from datetime import datetime,timedelta
endd=datetime.now() - timedelta(minutes = 182)
startt = datetime.now() - timedelta(minutes = 187)
start = startt.strftime("%Y-%m-%dT%H:%M:%SZ")
end = endd.strftime("%Y-%m-%dT%H:%M:%SZ")
edgerc = EdgeRc('/root/.edge')
section = 'log'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
result = s.get(urllib.parse.urljoin(baseurl, 'datastream-pull-api/v1/streams/8102/raw-logs?page=1&size=2000&start='+start+'&end='+end))
json_txt = result.json()
request_items=json_txt['data']
page_size = json_txt['metadata']['pageCount']
if page_size > 1 :
    for page_number in range(2,page_size):
        result = s.get(urllib.parse.urljoin(baseurl, 'datastream-pull-api/v1/streams/8102/raw-logs?page='+str(page_number)+'&size=2000&start='+start+'&end='+end))
        tmp=result.json()
        dat=tmp['data']
        request_items = request_items + dat
file_name = "/es_data/akamai/akamai_"+start.replace(':',"-")+"_"+end.replace(':',"-")+".gz"
#with open(file_name, 'w', encoding='utf-8') as f:
#    json.dump(request_items, f, ensure_ascii=False)
json_bytes = json.dumps(request_items).encode('utf-8')
with gzip.open(file_name, 'w') as f:
    f.write(json_bytes)
