import json

f= open('../raw/IBM_full_raw.json')

data = json.load(f)

f.close()

data = data['IBM']
res = dict()
for k,v in data.items():
    entry = dict()
    for dt, d in v.items():
        entry[dt] = float(d)
    res[k] = entry

final = {"IBM" : res}

out_file = open("../processed/IBM_full.json", "w") 

json.dump(final, out_file, indent = 6) 
out_file.close() 