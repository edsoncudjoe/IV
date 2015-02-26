import requests
import json

url = "http://192.168.0.101:8080/api/4"
auth = url + "/session?usr=SU&pwd=1487sbg"

catalog_id = []
content_iv_no = []

# Post login details to server. Load response into JSON
response = requests.get(auth)

auth_data = json.loads(response.text)
	
# get the session ID for future calls
sessionid = auth_data['data']['jsessionid']

# Get all available catalogs
catalogs = requests.get(url + "/catalogs;jsessionid=" + sessionid)


catalog_data = json.loads(catalogs.text)

# list of client group names plus associated CatDV ID numbers
catalog_id = [(i['groupName'], i['ID']) for i in catalog_data['data'] if i['ID'] > 1]

# Get client IV numbers

#def all_content(client_id):
content_raw = requests.get(url + '/clips;jsessionid=' + sessionid + '?filter=and((catalog.id)eq({}))&include=userFields'.format(catalog_id[0][1]))
content_data = json.loads(content_raw)
#	return content_data

def power_iv_gen():
	"""Searches for 'U7' and 'userFields' keys and yields the value of the 'U7' key."""
	count = 0
	try:
		for i in content_data['data']['items']:
			if 'userFields' in i.keys():
				if 'U7' in i['userFields']:
					count += 1
					#print 'Position: ' + count
					yield i['userFields']['U7']
	except:
		print('Error at position: {}'.format(count))

def collected_iv(content_data):
	try:	
		count = 0
		for i in range(len(content_data['data']['items'])):
			content_iv_no.append(next(pow_iv))
			count += 1
	except StopIteration:
		print('Collected {} Intervideo barcode numbers'.format(count))

	final = sorted(set(content_iv_no))
	return final
	

pow_iv = power_iv_gen()

# Add requests.delete() function to close session after search

#choice = raw_input('name: ')
#if choice == 'content':	
	# Content Media
#	content = all_content(catalog_id[1][1])
#elif choice == 'classic':
	# Classic Media
#	classic = get_IV_numbers(catalog_id[0][1])
#elif choice == 'ng':
	# NGTV
#	ngtv = get_IV_numbers(catalog_id[2][1])
#	ngtv.append(get_IV_numbers(catalog_id[3][1]))
#elif choice == 'power':
	# Power
#	power = get_IV_numbers(catalog_id[4][1])