#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design (Universidad Politecnica de Madrid)
Code with functions of widgets for Jupyter Notebook DEMO

:author: Javier Parra Paredes
"""

# Import Libraries
import ipywidgets as widgets
from helpers.constants import LinearCircuitSolver, AnnealerSolution
from fujitsu_tools.fujitsu_tools import TemperatureMode, AutoTuningMode, GraphicsDetailMode
from dadk.QUBOSolverCPU import *


class TestCircuitWidget:
	"""
	This class includes the widgets for selection of test_circuit and associated functions such as show schematic, show
	netlist or solution.
	By default,: TEST_CIRCUIT_1
	"""

	def __init__(self):

		# Test circuit selection
		self.test_circuit_widget = widgets.RadioButtons(
			options=[LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1, LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2,
			         LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3, LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4],
			description='Electronic circuit under test:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		print("########################### Selection of Test Circuit ###########################")
		display(self.test_circuit_widget)

	def show_circuit(self, test_circuit_path):
		"""
		It shows the circuit under test in png format
		:param test_circuit_path:
		:return:
		"""
		test_circuit_img = \
			LinearCircuitSolver.TestCircuits.get_test_circuit_image(self.test_circuit_widget.value)

		file = open(os.path.join(os.path.dirname(test_circuit_path), test_circuit_img), "rb")
		image = file.read()
		print("This is the schematic of the electronic circuit under test: " + self.test_circuit_widget.value)
		img = widgets.Image(value=image, format='png', width=500, height=600)
		display(img)

	def show_netlist(self, test_circuit_path):
		"""
		It shows the netlist information of the circuit under test in png format
		:param test_circuit_path:
		:return:
		"""
		test_circuit_netlist = \
			LinearCircuitSolver.TestCircuits.get_test_circuit_netlist_info(self.test_circuit_widget.value)

		file = open(os.path.join(os.path.dirname(test_circuit_path), test_circuit_netlist), "rb")
		image = file.read()
		print("This is the netlist information in SPICE format of the electronic circuit under test: " +
		      self.test_circuit_widget.value)
		img = widgets.Image(value=image, format='png')
		display(img)

	def show_solutions(self, test_circuit_path):
		"""
		It shows the netlist information of the circuit under test in png format
		:param test_circuit_path:
		:return:
		"""
		test_circuit_solution = \
			LinearCircuitSolver.TestCircuits.get_test_circuit_solution(self.test_circuit_widget.value)

		file = open(os.path.join(os.path.dirname(test_circuit_path), test_circuit_solution), "rb")
		image = file.read()
		print("These are the theoretical solutions obtained by LTSpice of the electronic circuit under test: " +
		      self.test_circuit_widget.value)
		img = widgets.Image(value=image, format='png')
		display(img)


class MethodWidget:
	"""
	This class includes the widget for selection of method (method 1/ METHOD_WITHOUT_SIGN or method 2/METHOD_WITH_SIGN).
	By Default: METHOD_WITHOUT_SIGN
	"""

	def __init__(self):

		# Method Selection
		self.method_widget = widgets.RadioButtons(
			options=[LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN, LinearCircuitSolver.Method.METHOD_WITH_SIGN],
			description='Method:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		display(self.method_widget)


class NumberOfQubits:
	"""
	This class includes the widget for selecting the number of qubits for integer and fractional parts. It is the same
	number for all the variables
	By default: 2 for integer part and 2 for fractional part, min=0, max=10
	"""

	def __init__(self):
		# Number of qubits for integer part selection
		self.number_of_integer_qubits_widget = widgets.IntSlider(
			value=2,
			min=0,
			max=10,
			step=1,
			description='Number of qubits for Integer part:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)
		# Number of qubits for fractional part selection
		self.number_of_fractional_qubits_widget = widgets.IntSlider(
			value=2,
			min=0,
			max=10,
			step=1,
			description='Number of qubits for Fractional part:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)

		display(self.number_of_integer_qubits_widget)
		display(self.number_of_fractional_qubits_widget)


class AnnealerSolver:
	"""
	This class includes the widget for selecting the annealer solver.
	By default, DWAVE_SIM
	"""

	def __init__(self):
		self.annealer_solver_widget = widgets.RadioButtons(
			options=[AnnealerSolution.DWAVE_SIM, AnnealerSolution.DWAVE_HYBRID_SOLVER, AnnealerSolution.DWAVE_QPU,
			         AnnealerSolution.FUJITSU_SIM],
			description='Annealer Solver:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		display(self.annealer_solver_widget)


class AnnealerSolverParameters:
	"""
	This class includes the widgets for configuring the specific parameters of the solver.
	The annealer solver is provided as input parameter to show only the specific parameters of the selected solver.
	"""

	def __init__(self, annealer_solver):

		########################## FUJITSU Digital Annealer (Simulator) Parameters #####################################

		# Number of reads for Fujitsu Digital Annealer Solver (by default 125, min=1, max=128)
		self.number_of_reads_fujitsu_widget = widgets.IntSlider(
			value=125,
			min=1,
			max=128,
			step=1,
			description='Number of Reads:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)

		# Number of iterations for Fujitsu Digital Annealer Solver (by default 1000, min=1, max=10000)
		self.number_of_iterations_fujitsu_widget = widgets.IntSlider(
			value=1000,
			min=1,
			max=10000,
			step=1,
			description='Number of Iterations:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)

		# Start Temperature for Fujitsu Digital Annealer Solver (by default, 0.01).
		self.start_temperature_fujitsu_widget = widgets.BoundedFloatText(
			value=0.01,
			description='Start Temperature:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# End Temperature for Fujitsu Digital Annealer Solver (by default, 0.000001).
		self.end_temperature_fujitsu_widget = widgets.BoundedFloatText(
			value=0.000001,
			description='End Temperature:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# Temperature Mode Selection for Fujitsu Digital Annealer Solver (by default, EXPONENTIAL)
		self.temperature_mode_fujitsu_widget = widgets.RadioButtons(
			options=[TemperatureMode.get_temperature_mode_str(TemperatureMode.EXPONENTIAL),
			         TemperatureMode.get_temperature_mode_str(TemperatureMode.INVERSE),
			         TemperatureMode.get_temperature_mode_str(TemperatureMode.INVERSE_ROOT)],
			description='Temperature mode:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# Temperature interval for Fujitsu Digital Annealer Solver (by default 1)
		self.temperature_interval_fujitsu_widget = widgets.BoundedFloatText(
			value=1.0,
			description='Temperature Interval:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# Offset Increase rate for Fujitsu Digital Annealer Solver (by default, 0.01)
		self.offset_increase_rate_fujitsu_widget = widgets.BoundedFloatText(
			value=0.01,
			description='Offset increase rate:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# Number of bits scaling for Fujitsu Digital Annealer Solver (by default, 62)
		self.number_of_bits_scaling_fujitsu_widget = widgets.IntSlider(
			value=62,
			min=1,
			max=62,
			step=1,
			description='Number of bits scaling:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)
		# Auto Tuning Mode Selection for Fujitsu Digital Annealer Solver (by default, AUTO_SCALING)
		self.auto_tuning_mode_fujitsu_widget = widgets.RadioButtons(
			options=[AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.AUTO_SCALING),
			         AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.NOTHING),
			         AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.SCALING),
			         AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.SAMPLING),
			         AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.AUTO_SCALING_AND_SAMPLING),
			         AutoTuningMode.get_auto_tuning_mode_str(AutoTuning.SCALING_AND_SAMPLING)],
			description='Auto Tuning Mode:',
			disabled=False,
			style={'description_width': 'initial'}
		)
		# Graphics Detail Mode for Fujitsu Digital Annealer Solver (by default, ALL)
		self.graphics_detail_mode_fujitsu_widget = widgets.RadioButtons(
			options=[GraphicsDetailMode.get_graphics_detail_str(GraphicsDetail.ALL),
			         GraphicsDetailMode.get_graphics_detail_str(GraphicsDetail.NOTHING),
			         GraphicsDetailMode.get_graphics_detail_str(GraphicsDetail.SINGLE)],
			description='Graphics Detail Mode:',
			disabled=False,
			style={'description_width': 'initial'}
		)

		########################## D-Wave Parameters #####################################
		# Number of reads for DWAVE Simulator and QPU Solver (by default 500, min=1, max=500)
		self.number_of_reads_dwave_widget = widgets.IntSlider(
			value=500,
			min=1,
			max=500,
			step=1,
			description='Number of Reads:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)
		# Chain Strength for DWAVE QPU Solver (by default 10, min=0, max=1000)
		self.chain_strength_dwave_widget = widgets.IntSlider(
			value=10,
			min=0,
			max=1000,
			step=1,
			description='Chain Strength:',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)
		# Annealing time for DWAVE QPU Solver in us (by default 20us, min=20(us), max=1800(us))
		self.annealing_time_us_dwave_widget = widgets.IntSlider(
			value=20,
			min=20,
			max=1800,
			step=1,
			description='Annealing Time (us):',
			disabled=False,
			continuous_update=False,
			orientation='horizontal',
			readout=True,
			readout_format='d',
			layout=widgets.Layout(width='50%'),
			style={'description_width': 'initial'}
		)

		# The specific parameters are displayed or not according to the annealer solver
		if annealer_solver == AnnealerSolution.FUJITSU_SIM:
			print("Fujitsu Digital Annealer (Simulator) Parameters:")
			display(self.number_of_reads_fujitsu_widget)
			display(self.number_of_iterations_fujitsu_widget)
			display(self.start_temperature_fujitsu_widget)
			display(self.end_temperature_fujitsu_widget)
			display(self.temperature_mode_fujitsu_widget)
			display(self.temperature_interval_fujitsu_widget)
			display(self.offset_increase_rate_fujitsu_widget)
			display(self.number_of_bits_scaling_fujitsu_widget)
			display(self.auto_tuning_mode_fujitsu_widget)
			display(self.graphics_detail_mode_fujitsu_widget)

		elif annealer_solver == AnnealerSolution.DWAVE_SIM:
			print("D-Wave Simulator Parameters:")
			display(self.number_of_reads_dwave_widget)
		elif annealer_solver == AnnealerSolution.DWAVE_QPU:
			print("D-Wave QPU Parameters:")
			display(self.number_of_reads_dwave_widget)
			display(self.chain_strength_dwave_widget)
			display(self.annealing_time_us_dwave_widget)
		elif annealer_solver == AnnealerSolution.DWAVE_HYBRID_SOLVER:
			print("D-Wave Hybrid Solver Parameters: N/A")
