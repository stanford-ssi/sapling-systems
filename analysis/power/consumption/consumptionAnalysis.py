import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import json

# load config data, power generation data
configFile = open('./configuration/config.json')
generationFile = open('/path/to/power/generation/data.json')
config = json.load(configFile)
generationData = json.load(generationFile)
configFile.close()
generationFile.close()

# make dictionary with power consumption for each mode
modesPowerRates = {k: v['power consumption']
                   for k, v in config['modes'].items()}

# make dictionary with power consumption for each phase
phasesPowerRates = {}
for phase, phaseConfig in config['phases'].items():
    powerTotal = 0
    if 'modes' in phaseConfig:
        for mode, onPercent in phaseConfig['modes'].items():
            powerTotal += modesPowerRates[mode] * onPercent
    phasesPowerRates[phase] = powerTotal

# graph data
times = map(lambda e: dt.datetime.strptime(
    e['Epoch'][:-10], '%b %d %Y %H:%M:%S'), generationData)
totalPower = map(lambda e: e['TotalPower'], generationData)
totalPowerSMA = np.convolve(totalPower, np.ones(24), 'valid') / 24  # 2hr SMA
totalPowerSMA = totalPowerSMA.tolist() + [sum(totalPower) / len(totalPower)]*(
    len(totalPower) - len(totalPowerSMA))  # pad with avg to make it the same length
idlePower = map(lambda e: modesPowerRates['idle'], generationData)
deploymentPower = map(lambda e: phasesPowerRates['deployment'], generationData)
operationsPower = map(
    lambda e: phasesPowerRates['mission operations'], generationData)
lowPower = map(
    lambda e: modesPowerRates['low power'], generationData)

plt.title("Power Consumption Analysis")
plt.xlabel('time')
plt.ylabel('power (w)')
plt.plot(times, totalPower, color='lightgreen', label="power generated")
plt.plot(times, totalPowerSMA, color='green', label="Generated SMA")
plt.plot(times, idlePower, color='orange', label='Idle')
plt.plot(times, operationsPower, color='blue', label="Mission ops")
plt.plot(times, lowPower, color='darkred', label="Low power")
# plt.plot(times, deploymentPower, color='pink', label='Deployment')

plt.legend()
plt.show()
