#!/usr/bin/python

import base64
import json
import urllib2
key = 1785
secret_key =  'cc8dc0f89a677a8aeb45e2d0a4351b765d684f68' 
base64string = base64.encodestring('%s:%s' % (key, secret_key))[:-1]  #[:-1] removes newline at end
http_headers = {'Authorization' : 'Basic %s' % base64string}          #HTTP basic authentication

request = urllib2.Request('https://api.picloud.com/r/1741/main_func',
                          data='url="http://127.0.0.1:8080"',
                          headers=http_headers)
response = urllib2.urlopen(request)
print response.read()
data = json.load(response)   #{"version": "0.1", "servers": ["https://api.picloud.com/"]}

