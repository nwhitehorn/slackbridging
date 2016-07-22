#!/usr/bin/env python

import os, cgi, requests, json, sys


# Bidirectional webhook links from one channel/domain pair to the incoming
# webhook for the other.

# This mirrors slackchannel1 on two slack domains (e.g. mydomain.slack.com)
# onto each other and mirrors slackchannel2 on mydomain to
# slackchannel2@conference.example.com on a Prosody server.

links = {
	'slackchannel1/mydomain': 'https://hooks.slack.com/services/foo/bar2'
	'slackchannel1/myotherdomain': 'https://hooks.slack.com/services/foo2/bar1'

	'slackchannel2/conference.example.com': ('https://hooks.slack.com/services/incoming/hook', '#slackchannel2'),
	'slackchannel2/mydomain': 'https://conference.example.com/webhook/slackchannel2',
}

if os.environ['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
	data = cgi.parse()
else:
	rawdata = json.loads(sys.stdin.read(int(os.environ['CONTENT_LENGTH'])))
	data = {}
	for k in rawdata.keys():
		data[k] = [rawdata[k]]

message = {'text': data['text'][0], 'username': data['user_name'][0]}

chatname = data['channel_name'][0] + '/' + data['team_domain'][0]
if chatname in links and 'bot_id' not in data: # Ignore missing chats and avoid relay loops
	if isinstance(links[chatname], tuple):
		url = links[chatname][0]
		message['channel'] = links[chatname][1]
	else:
		url = links[chatname]
	requests.post(url, json=message)

