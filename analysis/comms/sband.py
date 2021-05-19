#!/usr/bin/env python

# standard libraries
import os
import shutil
import subprocess

# third-party libraries
import numpy as np
import matplotlib.pyplot as plt
import pylink

sat_pattern = pylink.pattern_generator(3)

sat_rf_chain = [
    pylink.Element(name="Cables", gain_db=-0.05, noise_figure_db=0.75),
    pylink.Element(name="Filter", gain_db=-3.5, noise_figure_db=3.5),
    pylink.Element(name="Demodulator", gain_db=0, noise_figure_db=15),
]

gs_rf_chain = [
    pylink.Element(name="Cables", gain_db=-0.75, noise_figure_db=0.75),  # TODO measure
    pylink.Element(name="LNA", gain_db=35, noise_figure_db=2.75),  # TODO double check
    pylink.Element(name="Filter", gain_db=-3.5, noise_figure_db=3.5),
    pylink.Element(name="Demodulator", gain_db=0, noise_figure_db=15),
]

geometry = pylink.Geometry(
    apoapsis_altitude_km=450, periapsis_altitude_km=450, min_elevation_deg=20
)

sat_rx_antenna = pylink.Antenna(  # TODO figure out whether there is geometry and what pointing assumptions are made
    gain=3,
    polarization="RHCP",
    pattern=sat_pattern,  # TODO double check what this means
    rx_noise_temp_k=1000,
    is_rx=True,
    tracking=False,
)

sat_tx_antenna = pylink.Antenna(
    gain=3, polarization="RHCP", pattern=sat_pattern, is_rx=False, tracking=False
)

gs_rx_antenna = pylink.Antenna(
    pattern=pylink.pattern_generator(48),  # TODO what does this mean
    rx_noise_temp_k=300,
    polarization="RHCP",
    is_rx=True,
    tracking=True,
)

gs_tx_antenna = pylink.Antenna(gain=25, polarization="RHCP", is_rx=False, tracking=True)

sat_receiver = pylink.Receiver(
    rf_chain=sat_rf_chain, implementation_loss_db=2, name="Satellite SBand Receiver"
)

gs_receiver = pylink.Receiver(rf_chain=gs_rf_chain, name="Ground SBand Receiver")

gs_transmitter = pylink.Transmitter(
    tx_power_at_pa_dbw=23, name="Ground SBand Transmitter"
)

sat_transmitter = pylink.Transmitter(
    tx_power_at_pa_dbw=1.5, name="Satellite SBand Transmitter"
)

rx_interconnect = pylink.Interconnect(is_rx=True)


tx_interconnect = pylink.Interconnect(is_rx=False)

s_channel = pylink.Channel(
    bitrate_hz=500e3,  # TODO double check
    allocation_hz=5e6,  # TODO double check
    center_freq_mhz=2450.0,
    atmospheric_loss_db=0.5,
    ionospheric_loss_db=0.5,
    rain_loss_db=1,
    multipath_fading_db=0,
    polarization_mismatch_loss_db=3,
)

# defaults to DVB-S2X
modulation = pylink.Modulation(name="p2400 345.6")  # TODO add frequency hopping scheme

DOWNLINK = pylink.DAGModel(
    [
        geometry,
        gs_rx_antenna,
        sat_transmitter,
        sat_tx_antenna,
        gs_receiver,
        s_channel,
        rx_interconnect,
        tx_interconnect,
        modulation,
        pylink.LinkBudget(name="SBand Downlink", is_downlink=True),
    ]
)

UPLINK = pylink.DAGModel(
    [
        geometry,
        sat_rx_antenna,
        sat_receiver,
        gs_transmitter,
        gs_tx_antenna,
        s_channel,
        pylink.LinkBudget(name="SBand Uplink", is_downlink=False),
    ]
)
