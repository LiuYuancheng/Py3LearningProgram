import json
 
# Opening JSON file
f = open('test/countryCode.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list


res = dict((v,k) for k,v in data.items())

# Closing file
f.close()

with open('swapCC.json', 'w') as f2:
    f2.write(json.dumps(res))