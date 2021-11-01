#!/usr/bin/python
import requests
import urllib.parse
import json
import gzip
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from datetime import datetime,timedelta
timezone = 3 # if you are in GMT+3 timezone you should write 3
shift_to_utc = timezone*60
endd=datetime.now() - timedelta(minutes = shift_to_utc+2) # +2 
startt = datetime.now() - timedelta(minutes = shift_to_utc+7) # 5 minutes interval
start = startt.strftime("%Y-%m-%dT%H:%M:%SZ")
end = endd.strftime("%Y-%m-%dT%H:%M:%SZ")
edgerc = EdgeRc('~/.edge') #this is the authentication file you have downloaded from portal
stream_id= XXXXXX # this will be the stream id that you will obtain from the datastream list. 
section = 'Default'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
result = s.get(urllib.parse.urljoin(baseurl, 'datastream-pull-api/v1/streams/'+str(stream_id)+'/raw-logs?page=1&size=2000&start='+start+'&end='+end))
json_txt = result.json()
#print(json_txt)
request_items=json_txt['data']
page_size = json_txt['metadata']['pageCount']
if page_size > 1 :
    for page_number in range(2,page_size):
        result = s.get(urllib.parse.urljoin(baseurl, 'datastream-pull-api/v1/streams/'+str(stream_id)+'/raw-logs?page='+str(page_number)+'&size=20000&start='+start+'&end='+end))
        tmp=result.json()
        dat=tmp['data']
        request_items = request_items + dat
file_name = "akamai_"+start.replace(':',"-")+"_"+end.replace(':',"-")+".json"
with open(file_name, 'w', encoding='utf-8') as f:
        for item in request_items:
           json.dump(item,f,ensure_ascii=False)
           f.write('\n')
