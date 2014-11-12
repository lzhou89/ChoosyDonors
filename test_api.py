import requests

###Proposal Info###

# r = requests.get(
	# '''http://api.donorschoose.org/common/json_feed.html?index=0&max=50&subject1=-1&APIKey=DONORSCHOOSE''')
# r = r.json()
# prop = r['proposals']
# data = ''
# print prop[0]
# for i in range(len(prop)):
# 	data += prop[i]+'/n'

# out_file = open('data.csv', 'w')
# out_file.write(prop)

# out_file.close()

###Donor Info###
# r = requests.get(
# 	'''http://api.donorschoose.org/common/json-donor.html?donorid=47474&APIKey=DONORSCHOOSE''')

###Teacher Info###
# r = requests.get(
# 	'''http://api.donorschoose.org/common/json-teacher.html?teacher=139499&APIKey=DONORSCHOOSE''')

###Giving Pages###
# r = requests.get(
# 	'''http://api.donorschoose.org/common/json_challenge.html?APIKey=DONORSCHOOSE&id=25298''')

###School Info###
r = requests.get(
	'''http://api.donorschoose.org/common/json_school.html?school=1675&APIKey=DONORSCHOOSE''')

r = r.json()
print r