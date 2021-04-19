import json
import datetime as dt

generationFile = open('../generation/output/powerGenerationData.json')
generationData = json.load(generationFile)
generationFile.close()

outputJson = []
time = dt.datetime(2021, 1, 1)
for day in range(14):
    for e in generationData:
        e['Epoch'] = time.strftime('%b %d %Y %H:%M:%S') + ".000000000"
        outputJson.append(e.copy())
        time += dt.timedelta(0, 300)  # add 5 min

with open('powerGeneration14day.json', 'w') as f:
    json.dump(outputJson, f, indent=2)
