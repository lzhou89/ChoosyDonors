import csv

states = {}
with open('static/data/teacher_ratio.csv', 'rb') as csvfile:
	all_ratios = csv.reader(csvfile, delimiter=',')
	next(all_ratios)
	ratios = []
	for line in all_ratios:
		ratios.append(float(line[1]))
	max_ratio = max(ratios)
	min_ratio = min(ratios)
	csvfile.seek(0)
	next(all_ratios)
	for line in all_ratios:
		n_ratio = (float(line[1])-min_ratio)*100/(max_ratio-min_ratio)
		states[line[0]] = [n_ratio]

with open('static/data/state_info.csv', 'rb') as csvfile:
	info = csv.reader(csvfile, delimiter=',')
	next(info)
	for line in info:
		states[line[0]].extend([float(line[1]), 100-float(line[2])])
		if line[3]:
			states[line[0]].append(100-float(line[3]))

zips = {}
with open('static/data/crime.csv') as csvfile:
	crime_rates = csv.reader(csvfile, delimiter=',')
	rates = []
	for line in crime_rates:
		if line[1]:
			rates.append(float(line[1]))
	max_rate = max(rates)
	min_rate = min(rates)
	csvfile.seek(0)
	for line in crime_rates:
		if line[1]:
			n_rate = (float(line[1])-min_rate)*100/(max_rate-min_rate)
			zips[line[0]] = [n_rate]

with open('static/data/pov_levels.csv') as csvfile:
	pov_levels = csv.reader(csvfile, delimiter=',')
	next(pov_levels)
	for line in pov_levels:
		if line[0] in zips:
			zips[line[0]].append(float(line[1]))
		else:
			zips[line[0]] = [float(line[1])]

# print states
# print zips

zip_state = {} #zip code: state
with open('static/data/zips.csv') as csvfile:
	all_zips = csv.reader(csvfile, delimiter=',')
	for line in all_zips:
		zip_state[line[0]] = line[1]

# print zip_state
all_zips = zip_state.keys() #all zip codes
# print all_zips

all_factors = {}

for item in all_zips: #a zip code
	# print item
	all_factors[item] = states[zip_state[item]] #zip_state[item]->state abbrev
	if item in zips:
		all_factors[item] = all_factors[item]+zips[item]

# print all_factors['38347']
# print zip_state['38347']
# print zips['38347']
# print states['TN']

keys = all_factors.keys()

with open('static/impact.csv', 'w') as file:
	for key in keys:
		factors = all_factors[key]
		print factors
		score = sum(factors)/len(factors)
		file.write(key+","+str(score)+"\n")