#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design (Universidad Politecnica de Madrid)
Code with upper level functions, independent of selected annealer solver

:author: Javier Parra Paredes
"""

# Import Libraries
from fujitsu_tools import fujitsu_tools
from dwave_tools import dwave_tools
from helpers.constants import AnnealerSolution
from sympy import *
from math import ceil
import matplotlib.pyplot as plt


def get_solution(annealer_solution, number_qubits_used, qubo_matrix, num_reads,
                 dwave_chain_strength=None,
                 dwave_annealing_time_us=None,
                 fujitsu_number_iterations=None, fujitsu_temperature_start=None, fujitsu_temperature_end=None,
                 fujitsu_temperature_mode=None, fujitsu_temperature_interval=None, fujitsu_offset_increase_rate=None,
                 fujitsu_scaling_bit_precision=None, fujitsu_auto_tuning=None, fujitsu_graphics=None):
	"""
	This is an upper level function which abstracts the selected annealer solver. All the parameters are provided
	(initialized to None) and the specific parameters for the selected annealer solver shall be passed.
	:param annealer_solution: annealer solver (DWAVE_SIM, DWAVE_HYBRID_SOLVER, DWAVE_QPU, FUJITSU_SIM)
	:param number_qubits_used: number of qubits for integer and fractional parts of each variable (for all solvers)
	:param qubo_matrix: qubo matrix (for all solvers)
	:param num_reads: number of reads (for all solvers, although not required for DWAVE Hybrid Solver)
	:param dwave_chain_strength: chain strength for DWAVE_QPU
	:param dwave_annealing_time_us: annealing time for DWAVE_QPU
	:param fujitsu_number_iterations: Number of Iterations (only for FUJITSU_SIM)
	:param fujitsu_temperature_start: start temperature (only for FUJITSU_SIM)
	:param fujitsu_temperature_end: end temperature (only for FUJITSU_SIM)
	:param fujitsu_temperature_mode: temperature mode (only for FUJITSU_SIM)
	:param fujitsu_temperature_interval: temperature interval (only for FUJITSU_SIM)
	:param fujitsu_offset_increase_rate: offset increase rate (only for FUJITSU_SIM)
	:param fujitsu_scaling_bit_precision: scaling bit precision (only for FUJITSU_SIM)
	:param fujitsu_auto_tuning: auto tuning mode (only for FUJITSU_SIM)
	:param fujitsu_graphics: graphics detail mode (only for FUJITSU_SIM)
	:return: it returns the raw response provided by the annealer solver.
	"""

	# Annealer solver function is called with its specific parameters, according to selected solver
	if annealer_solution == AnnealerSolution.FUJITSU_SIM:
		response = fujitsu_tools.get_fujitsu_solution(annealer_solution=annealer_solution,
		                                              total_num_qubits=number_qubits_used, qubo_matrix=qubo_matrix,
		                                              num_reads=num_reads, number_iterations=fujitsu_number_iterations,
		                                              temperature_start=fujitsu_temperature_start,
		                                              temperature_end=fujitsu_temperature_end,
		                                              temperature_mode=fujitsu_temperature_mode,
		                                              temperature_interval=fujitsu_temperature_interval,
		                                              offset_increase_rate=fujitsu_offset_increase_rate,
		                                              scaling_bit_precision=fujitsu_scaling_bit_precision,
		                                              auto_tuning=fujitsu_auto_tuning,
		                                              graphics=fujitsu_graphics)

	elif annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER or \
			annealer_solution == AnnealerSolution.DWAVE_QPU:

		response = dwave_tools.get_dwave_solution(annealer_solution=annealer_solution,
		                                          total_num_qubits=number_qubits_used, qubo_matrix=qubo_matrix,
		                                          num_reads=num_reads, chain_strength=dwave_chain_strength,
		                                          annealing_time_us=dwave_annealing_time_us)
	else:
		raise Exception("Annealer Solution not found : {}".format(annealer_solution))

	return response


def get_results(annealer_solution, x_matrix, method, response, num_qubits_dict):
	"""
	This function rebuilds the values of the variables from the response provided by annealer solver. It is an upper
	level function
	:param annealer_solution: selected annealer solver
	:param x_matrix: x variables (symbolic) as list of variables names
	:param method: method used (method 1/METHOD_WITHOUT_SIGN or Method 2/METHOD_WITH_SIGN)
	:param response: response (raw) provided by the annealer solver
	:param num_qubits_dict: number of qubits for integer and fractional parts of each variable
    :return: it returns a dictionary with the processed information of the results, ordered with this format (result_1
    is the minimum energy solution obtained:
    Example:
    {'result_1': {V1: 3, V2: 1, I_V1: -2, 'occurrences': 73, 'energy': -9.0},
    'result_2': {V1: 3, V2: 1, I_V1: -1, 'occurrences': 23, 'energy': -8.0}, etc
	"""
	if annealer_solution == AnnealerSolution.FUJITSU_SIM:

		data = fujitsu_tools.process_fujitsu_results(list_of_variables=x_matrix, method=method, response=response,
		                                             num_qubits_dict=num_qubits_dict)

	elif annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER or \
			annealer_solution == AnnealerSolution.DWAVE_QPU:

		data = dwave_tools.process_dwave_results(annealer_solution=annealer_solution, list_of_variables=x_matrix,
		                                         method=method, response=response,
		                                         num_qubits_dict=num_qubits_dict)
	else:
		raise Exception("Annealer Solution not found : {}".format(annealer_solution))

	return data


def get_expected_results_from_file(expected_results_file_path):
	"""
	This function gets the expected results provided as .txt file in the folder of input data of the circuit under test
	:param expected_results_file_path: file path where the txt file is located with the solutions
	:return: It returns a dictionary with the expected results with this format as example:
	{V1: 3, V2: 1, I_V1: -2}
	"""
	expected_results_dict = {}
	expected_results_file = open(expected_results_file_path, 'r')

	# Solutions .txt file is processed and a dictionary is returned with the symbolic name of each variable and expected
	# result
	lines = expected_results_file.readlines()
	for line in lines:
		key_raw = line.split('=')[0]
		key = key_raw.strip()
		value_raw = line.split('=')[1]
		value = value_raw.strip()

		expected_results_dict[Symbol(key)] = float(value)

	return expected_results_dict


def get_error_lsb_wrt_expected_results(expected_results_dict, data_dict, num_qubits_dict):
	"""
	This function returns the errors of each variable with respect to theoretical values.
	:param expected_results_dict: dictionary with expected result of each variable (value obtained by LTSpice).
	:param data_dict: result with the format returned by function get_results
	:param num_qubits_dict: dictionary with the number of qubits (integer and fractional parts) for calculation of error
	 in LSBs
	:return: It returns 3 dictionaries with 3 types of errors:
	- Absolute error: obtained value - expected value
	- Percentage error: 100 * (obtained value - expected value)/expected value
	- Error in LSBs: ceil(abs((obtained value - expected_result) / lsb_value))
	"""
	absolute_error_dict = {}
	percentage_error_dict = {}
	lsb_dict = {}

	# Go through all the variables
	for key in expected_results_dict:
		expected_result = expected_results_dict[key]
		absolute_error_dict[key] = data_dict[key] - expected_result

		# calculate difference wrt expected results of LSBs
		# LSB value is calculated
		lsb_value = pow(2, -num_qubits_dict[key]["FRACTIONAL"])
		lsb_dict[key] = ceil(abs((data_dict[key] - expected_result) / lsb_value))

		if expected_result != 0:
			# Calculate error if expected value is different from zero to avoid a division by null.
			percentage_error_dict[key] = 100 * (data_dict[key] - expected_result) / expected_result
		else:
			# if expected value is 0, percentage error is N/A
			percentage_error_dict[key] = "N/A"

	return absolute_error_dict, percentage_error_dict, lsb_dict


def plot_errors(error_dict, title):
	"""
	It plots the error of each variable in a bar chart to be shown in the demo
	:param error_dict: dictionary with the error of each variable. It can be absolute error, percentage error or
	difference in LSBs
	:param title: string to be provided externally, according to "Absolute Error", Percentage Error" or
	"Difference in LSBs"
	:return:
	"""

	fig, ax = plt.subplots()

	list_of_variable_name_str = []
	list_of_values_str = []
	list_of_values_float = []

	for variable_name_symbol in error_dict.keys():
		if error_dict[variable_name_symbol] != "N/A":
			list_of_variable_name_str.append(str(variable_name_symbol))
			list_of_values_str.append(str(round(error_dict[variable_name_symbol], 2)))
			list_of_values_float.append(round(error_dict[variable_name_symbol], 2))
		else:
			print("In " + title + "plot, variable " + str(variable_name_symbol) + " can not be plotted : N/A")

	ax.bar(list_of_variable_name_str, list_of_values_float)
	ax.set_ylabel(title)
	ax.set_title(title + ' with respect to Theoretical values')

	for i in range(len(list_of_variable_name_str)):
		plt.text(i, list_of_values_float[i], list_of_values_str[i], ha='center')

	plt.show()
