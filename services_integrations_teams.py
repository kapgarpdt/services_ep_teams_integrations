#!/usr/bin/env python
import json
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

csvfile = "services_teams_integrations_ep_timestamp.csv"
with open(csvfile, "a") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow( ['service_name', 'escalation_policies', 'teams', 'integrations', 'last_incident_timestamp'])
	

API_ACCESS_KEY=''
BASE_URL = 'https://api.pagerduty.com'
HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=API_ACCESS_KEY),
		'Content-type': 'application/json'
	}

	
def get_services():
	more = True
	all_services = requests.get(BASE_URL + '/services/' + '?&include%5B%5D=escalation_policies&include%5B%5D=teams&include%5B%5D=integrations', headers=HEADERS)
	while more:
		for service in all_services.json()['services']:
			team_names = ''
			for team in service['teams']:
				team_names= team['summary']
			integration_names = []
			for integration in service['integrations']:
				integration_names += [integration['summary']]
			with open(csvfile, 'a') as output:
				writer = csv.writer(output, lineterminator='\n')
				row = [service['name'], service['escalation_policy']['summary'], str(team_names), str(json.dumps(integration_names)), service['last_incident_timestamp']]
				#print(row)
				writer.writerow(row)
		more = all_services.json()['more']
		offset = all_services.json()['offset'] + all_services.json()['limit']
		params = {
		'offset':offset
		}
		print(offset)
		all_services = requests.get(BASE_URL + '/services', headers=HEADERS, params=params)
		
	    	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	get_services()
	

if __name__=='__main__':
	sys.exit(main())
