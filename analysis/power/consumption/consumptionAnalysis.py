import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import json
import argparse


def toDatetime(epoch):
    return dt.datetime.strptime(epoch[:-10], '%b %d %Y %H:%M:%S')


def simulate(config):
    mode = "payload"  # initial mode
    batteryCharge = config['battery']['initialCharge']
    batteryCapacity = config['battery']['capacity']
    batteryGraph = [batteryCharge]
    modeLog = [mode]

    for i, current in enumerate(generationData):
        if i == 0:
            continue
        previous = generationData[i-1]
        if batteryCharge < 5:
            mode = "low power"
        if batteryCharge < 10:
            mode = "recharge"
        elif batteryCharge > batteryCapacity * 0.95:
            mode = "payload"

        tDelta = (toDatetime(current['Epoch']) -
                  toDatetime(previous['Epoch'])).seconds/3600.0
        batteryCharge -= modesPowerRates[mode] * tDelta
        batteryCharge += (current['TotalPower'] +
                          previous['TotalPower']) / 2 * tDelta
        batteryGraph.append(batteryCharge)
        modeLog.append(mode)

    return batteryGraph, modeLog


def stats(modeLog):
    length = float(len(modeLog))
    stats = {}
    for mode in config['modes'].keys():
        stats[mode] = {'percentOn': modeLog.count(mode) / length}
    return stats


# command line options
parser = argparse.ArgumentParser(
    description='Graph power usage based on a config file')
parser.add_argument('config', metavar='C', type=str,
                    help='Path to a config json file. See documentation for schema')
parser.add_argument('generation_data', metavar='D', type=str,
                    help='Path to a power generation analysis json file')

args = parser.parse_args()
argsDict = vars(args)

configFilePath = argsDict['config']
generationFilePath = argsDict['generation_data']

# load config data, power generation data
configFile = open(configFilePath)
generationFile = open(generationFilePath)
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

# graph
graphConfig = config['graph']
times = map(lambda e: toDatetime(e['Epoch']), generationData)

plt.title("Power Consumption Analysis")
plt.xlabel('time')
plt.ylabel('power (w)')

# battery simulation and graph
if graphConfig['battery charge']:
    batteryGraph, modeLog = simulate(config)
    plt.plot(times, batteryGraph, color='blue', label='battery charge')
    print("battery simulation stats")
    print(stats(modeLog))

# power generation graphs
totalPower = []
if graphConfig['power generated']:
    totalPower = map(lambda e: e['TotalPower'], generationData)
    plt.plot(times, totalPower, color='lightgreen', label="power generated")
if graphConfig['power generated SMA']:
    if not totalPower:
        totalPower = map(lambda e: e['TotalPower'], generationData)
    totalPowerSMA = np.convolve(
        totalPower, np.ones(24), 'valid') / 24  # 2hr SMA
    totalPowerSMA = totalPowerSMA.tolist() + [sum(totalPower) / len(totalPower)]*(
        len(totalPower) - len(totalPowerSMA))  # pad with avg to make it the same length
    plt.plot(times, totalPowerSMA, color='green', label="power generated SMA")

# graph modes:
for mode, on in graphConfig['modes'].items():
    if on:
        plot = map(
            lambda e: modesPowerRates[mode], generationData)
        plt.plot(times, plot, label=mode)

# graph phases:
for phase, on in graphConfig['phases'].items():
    if on:
        plot = map(
            lambda e: phasesPowerRates[phase], generationData)
        plt.plot(times, plot, label=phase)

plt.legend()
plt.show()
