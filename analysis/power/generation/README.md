# Power Generation

The `SolarPowerGeneration` FreeFlyer MissionPlan simulates a CubeSat and determines its power generation over time based on the provided configuration. The user may specify the length and timestep of the simulation, configure an arbitrary number of ground stations, and configure a spacecraft with an arbitrary number of solar panels. The output consists of the power at each timestep through the simulation, whether or not the spacecraft is in Earth's Shadow, and the vector to the Sun in the Spacecraft Body Coordinate System.

## Organization

`include/` - generic FreeFlyer Procedures for reusability
`configuration/` - configuration files for the MissionPlan
`output/` - output files for the MissionPlan (gitignored)
`SolarPowerGeneration.txt` - text file containing all of the FreeForm (FreeFlyer script) definite the analysis.
