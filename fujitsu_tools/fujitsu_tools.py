#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design  (Universidad Politecnica de Madrid)
Code with functions used with Fujitsu solver (Digital Annealer Simulator)

:author: Javier Parra Paredes
"""

# Import libraries
from dadk.QUBOSolverCPU import *
from dadk.QUBOSolverDAv2 import *
from helpers.variables import get_qubits_per_variable, get_value
from helpers.constants import AnnealerSolution


class TemperatureMode:
	"""
	This class defines the Temperature Mode parameter (Exponential, Inverse or Inverse Root)
	"""
	EXPONENTIAL = 0     # reduce temperature by factor (1-temperature_decay) every temperature_interval steps
	INVERSE = 1         # reduce temperature by factor (1-temperature_decay*temperature) every temperature_interval steps
	INVERSE_ROOT = 2    # reduce temperature by factor (1-temperature_decay*temperature^2) every temperature_interval steps

	@staticmethod
	def get_temperature_mode_str(temperature_mode_int):
		"""
		This function returns the temperature mode in string format (provided the mode in integer as parameter)
		:param temperature_mode_int: temperature mode in integer format (0, 1 or 2)
		:return: temperature mode in string format
		"""
		d = {
			TemperatureMode.EXPONENTIAL: "EXPONENTIAL",
			TemperatureMode.INVERSE: "INVERSE",
			TemperatureMode.INVERSE_ROOT: "INVERSE_ROOT",
		}
		return d[temperature_mode_int]

	@staticmethod
	def get_temperature_mode_int(temperature_mode_str):
		"""
		This function returns the temperature mode in integer format (provided the mode in string as parameter)
		:param temperature_mode_str: temperature mode in string forma
		:return: temperature mode in integer format
		"""
		d = {
			"EXPONENTIAL": TemperatureMode.EXPONENTIAL,
			"INVERSE": TemperatureMode.INVERSE,
			"INVERSE_ROOT": TemperatureMode.INVERSE_ROOT
		}
		return d[temperature_mode_str]


class AutoTuningMode:
	"""
	This class defines the functions to handle Auto Tuning Mode parameter
	Following methods for scaling qubo and determining temperatures are available:
		AutoTuning.NOTHING: no action
		AutoTuning.SCALING: scaling_factor is multiplied to qubo, temperature_start, temperature_end
		and offset_increase_rate.
		AutoTuning.AUTO_SCALING: A maximum scaling factor w.r.t. scaling_bit_precision is multiplied to qubo,
		temperature_start, temperature_end and offset_increase_rate.
		AutoTuning.SAMPLING: temperature_start, temperature_end and offset_increase_rate are automatically determined.
		AutoTuning.AUTO_SCALING_AND_SAMPLING: Temperatures and scaling factor are automatically determined and applied.
	"""

	@staticmethod
	def get_auto_tuning_mode_str(auto_tuning_mode_int):
		"""
		This function returns Auto Tuning Mode parameter in string format
		:param auto_tuning_mode_int: Auto Tuning Mode in integer format
		:return: Auto Tuning Mode in string format
		"""
		d = {
			AutoTuning.NOTHING: "NOTHING",
			AutoTuning.SCALING: "SCALING",
			AutoTuning.AUTO_SCALING: "AUTO_SCALING",
			AutoTuning.SAMPLING: "SAMPLING",
			AutoTuning.AUTO_SCALING_AND_SAMPLING: "AUTO_SCALING_AND_SAMPLING",
			AutoTuning.SCALING_AND_SAMPLING: "SCALING_AND_SAMPLING"
		}
		return d[auto_tuning_mode_int]

	@staticmethod
	def get_auto_tuning_mode_int(auto_tuning_mode_str):
		"""
		This function returns Auto Tuning Mode parameter in integer format
		:param auto_tuning_mode_str: Auto Tuning Mode in string format
		:return: Auto Tuning Mode in integer format
		"""
		d = {
			"NOTHING": AutoTuning.NOTHING,
			"SCALING": AutoTuning.SCALING,
			"AUTO_SCALING": AutoTuning.AUTO_SCALING,
			"SAMPLING": AutoTuning.SAMPLING,
			"AUTO_SCALING_AND_SAMPLING": AutoTuning.AUTO_SCALING_AND_SAMPLING,
			"SCALING_AND_SAMPLING": AutoTuning.SCALING_AND_SAMPLING
		}
		return d[auto_tuning_mode_str]


class GraphicsDetailMode:
	"""
	This class defines the functions to handle Graphics Detail Mode parameter
	"""

	@staticmethod
	def get_graphics_detail_str(graphics_detail_int):
		"""
		This function returns Graphics Detail Mode parameter in string format
		:param graphics_detail_int: Graphics Detail Mode in integer format
		:return: Graphics Detail Mode in string format
		"""
		d = {
			GraphicsDetail.NOTHING: "NOTHING",
			GraphicsDetail.SINGLE: "SINGLE",
			GraphicsDetail.ALL: "ALL"
		}
		return d[graphics_detail_int]

	@staticmethod
	def get_graphics_detail_int(graphics_detail_str):
		"""
		This function returns Graphics Detail Mode parameter in integer format
		:param graphics_detail_str: Graphics Detail Mode in string format
		:return: Graphics Detail Mode in integer format
		"""
		d = {
			"NOTHING": GraphicsDetail.NOTHING,
			"SINGLE": GraphicsDetail.SINGLE,
			"ALL": GraphicsDetail.ALL
		}
		return d[graphics_detail_str]


def get_fujitsu_solution(annealer_solution, total_num_qubits, qubo_matrix, num_reads=125, number_iterations=500,
                         temperature_start=0.01, temperature_end=0.00001, temperature_mode=TemperatureMode.EXPONENTIAL,
                         temperature_interval=1, offset_increase_rate=0.0005, scaling_bit_precision=62,
                         auto_tuning=AutoTuning.AUTO_SCALING, graphics=GraphicsDetail.ALL):
	"""
	This function receives the QUBO matrix obtained previously and according and sets the configuration of Fujitsu
	Digital Annealer Simulator (QUBO terms, and specific parameters)
	:param annealer_solution: Fujitsu Digital Annealer Simulator. This parameter is used if remote Fujitsu Digital
	Annealer is available in the future
	:param total_num_qubits: total number of qubits used in QUBO matrix
	:param qubo_matrix: QUBO matrix
	:param num_reads: total number of reads (by default, 125, max 128)
	:param number_iterations:
	:param temperature_start: temperature start (by default 0.01)
	:param temperature_end: temperature end (by default 0.00001)
	:param temperature_mode: how the temperature drops (by default, EXPONENTIAL)
	:param temperature_interval: temperature interval (by default, 1)
	:param offset_increase_rate: offset increase rate (by default 0.0005, if 0, not used)
	:param scaling_bit_precision: scaling bit precision (by default 62)
	:param auto_tuning: Auto Tuning mode (by default, AUTO_SCALING)
	:param graphics: Graphics Detail Mode (by default, ALL)
	:return: it returns the response in raw provided by Fujitsu solver
	"""
	my_poly = BinPol()

	# The terms to program in the annealer solver are split into 2: linear and quadratic terms

	# linear terms (diagonal terms of QUBO matrix)
	for i in range(total_num_qubits):
		my_poly.set_term(qubo_matrix[i][i], (i,))

	#  quadratic terms (off - upper diagonal terms of QUBO matrix)
	for i in range(total_num_qubits - 1):
		for j in range(i + 1, total_num_qubits):
			if qubo_matrix[i][j] != 0:
				my_poly.set_term(qubo_matrix[i][j], (i, j))

	if annealer_solution == AnnealerSolution.FUJITSU_SIM:
		solver = QUBOSolverCPU(
			number_iterations=number_iterations,  # Total number of iterations per run.
			number_runs=num_reads,  # Number of stochastically independent runs.
			temperature_start=temperature_start,  # Start temperature of the annealing process.
			temperature_end=temperature_end,  # End temperature of the annealing process.
			temperature_mode=temperature_mode,  # 0, 1, or 2 to define the cooling curve
			temperature_interval=temperature_interval,  # Number of iterations keeping temperature constant.
			offset_increase_rate=offset_increase_rate,
			# Increase of dynamic offset when no bit selected. Set to 0.0 to switch off dynamic energy feature.
			graphics=graphics,  # Switch on graphics output.
			auto_tuning=auto_tuning,
			scaling_bit_precision=scaling_bit_precision
		)
	else:
		raise Exception("Annealer not found : {}".format(annealer_solution))

	solution_list = solver.minimize(my_poly)
	# Print Execution time and solutions in raw provided by Fujitsu Digital Annealer Simulator
	print(KEYWORD_EXECUTION_TIME, solution_list.solver_times.duration_execution)
	print(solution_list)

	return solution_list


def process_fujitsu_results(list_of_variables, method, response, num_qubits_dict):
	"""
	This function processes the response (raw) provided by Fujitsu Digital Annealer Simulator and rebuilds the values
	of the variables from the qubit values obtained in the response.
	:param list_of_variables: list of variables (x vector), in symbolic format
	:param method: method used (method 1 or same number of qubits for integer and fractional parts or method 2 or one
    qubit dedicated to the sign and the rest for the absolute value)
	:param response: response provided by Fujitsu Digital Annealer Simulator
    :param num_qubits_dict: information of number of qubits used for integer/fractional part of each variable.
    :return: it returns a dictionary with the processed information of the results, ordered with this format (result_1
    is the minimum energy solution obtained:
    Example:
    {'result_1': {V1: 3, V2: 1, I_V1: -2, 'occurrences': 73, 'energy': -9.0},
    'result_2': {V1: 3, V2: 1, I_V1: -1, 'occurrences': 23, 'energy': -8.0}, etc
	"""

	qubit_list_per_variable_dict, number_qubits_used = get_qubits_per_variable(list_of_variables=list_of_variables,
	                                                                           method=method,
	                                                                           num_qubits_dict=num_qubits_dict)

	variable_value_dict = {}

	result_index = 1

	for solution in response.solutions:
		raw_values_dict = {}
		for i, qubit_value in zip(range(0, len(solution.configuration)), solution.configuration):
			raw_values_dict['q' + str(i + 1)] = qubit_value
		energy = solution.energy
		num_occurrences = solution.frequency

		result_dict = {}

		for variable_index in range(0, len(list_of_variables)):

			# For each variable, it calls to a function "get_value" which rebuilds the value of the variable. This
			# function requires the method used (method 1 or 2), raw values dictionary (qubits values), number of qubits
			# of each variable used (integer and fractional parts) and assignment of qubits per each variable.
			result_dict[list_of_variables[variable_index]] = \
				get_value(method, raw_values_dict, num_qubits_dict[list_of_variables[variable_index]],
				          qubit_list_per_variable_dict[list_of_variables[variable_index]])

		result_dict["occurrences"] = num_occurrences
		result_dict["energy"] = energy

		variable_value_dict["result_" + str(result_index)] = result_dict
		result_index += 1

	# A dictionary with the results already converted is returned (see format in the description of the function above)
	return variable_value_dict
