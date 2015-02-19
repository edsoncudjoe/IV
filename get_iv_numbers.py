import requests
import json

url = "http://192.168.0.101:8080/api/4"
auth = url + "/session?usr=SU&pwd=1487sbg"

catalog_id = []

# Post login details to server. Load response into JSON
response = requests.get(auth)

auth_data = json.loads(response.text)
	
# get the session ID for future calls
sessionid = auth_data['data']['jsessionid']
# Get all available catalogs
catalogs = requests.get(url + "/catalogs;jsessionid=" + sessionid)


catalog_data = json.loads(catalogs.text)
catalog_id = [(i['groupName'], i['ID']) for i in catalog_data['data'] if i['ID'] > 1]

def get_IV_numbers(client):
	# Get Content Media IV numbers
	content_raw = requests.get(url + '/clips;jsessionid=' + sessionid + '?filter=and((catalog.id)eq({}))&include=userFields'.format(client))
	# REECEIVNG POSSIBLE SERVER ERROR AT THIS POINT. 
	content_data = json.loads(content_raw.text)

	#if there are any keys called userFields and there is a U7 in those keys, add the value of the U7 key to a list. 
	content_iv_no = [i['userFields']['U7'] for i in content_data['data']['items'] if 'userFields' in i.keys() if 'U7' in i['userFields']]
	final = sorted(set(content_iv_no))
	
	return final


choice = raw_input('name: ')
if choice == 'content':	
	# Content Media
	content = get_IV_numbers(catalog_id[1][1])
elif choice == 'classic':
	# Classic Media
	classic = get_IV_numbers(catalog_id[0][1])
elif choice == 'ng':
	# NGTV
	ngtv = get_IV_numbers(catalog_id[2][1])
	ngtv.append(get_IV_numbers(catalog_id[3][1]))
elif choice == 'power':
	# Power
	power = get_IV_numbers(catalog_id[4][1])