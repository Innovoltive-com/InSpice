####################################################################################################

import numpy as np

import matplotlib.pyplot as plt

####################################################################################################

import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice.Plot.BodeDiagram import bode_diagram
from InSpice import Circuit, Simulator, plot
from InSpice.Unit import *

from OperationalAmplifier import BasicOperationalAmplifier

#f# literal_include('OperationalAmplifier.py')

####################################################################################################

circuit = Circuit('Operational Amplifier')

# AC 1 PWL(0US 0V  0.01US 1V)
circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=1@u_V)
circuit.subcircuit(BasicOperationalAmplifier())
circuit.X('op', 'BasicOperationalAmplifier', 'in', circuit.gnd, 'out')
circuit.R('load', 'out', circuit.gnd, 470@u_Ω)

simulator = Simulator.factory()
simulation = simulator.simulation(circuit, temperature=25, nominal_temperature=25)
analysis = simulation.ac(start_frequency=1@u_Hz, stop_frequency=100@u_MHz, number_of_points=5,  variation='dec')

figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

plt.title("Bode Diagram of an Operational Amplifier")
bode_diagram(axes=(ax1, ax2),
             frequency=analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.out)),
             phase=np.angle(analysis.out, deg=False),
             marker='.',
             color='blue',
             linestyle='-',
            )
plt.tight_layout()
plt.show()

#f# save_figure('figure', 'operational-amplifier.png')
