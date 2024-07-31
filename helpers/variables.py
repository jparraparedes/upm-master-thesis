#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design (Universidad Politecnica de Madrid)
Code with functions to handle variables (x vector)

:author: Javier Parra Paredes
"""

# Import Libraries
from helpers.constants import LinearCircuitSolver


def get_qubits_per_variable(list_of_variables, method, num_qubits_dict):
	"""
	This function returns a list of qubits used for each variable and the total number of qubits for all variables
	:param list_of_variables: list of variables in symbolic format (x matrix)
	:param method: Method 1 or same number of qubits for positive and negative values, Method 2 or one qubit for the
	sign and the rest of qubits for absolute value
	:param num_qubits_dict: dictionary with the number of qubits for integer and fractional parts of each variable.
	Currently, the same number of qubits for all variables
	:return: a dictionary with a list of qubits used for each variable and the total number of qubits used for all
	variables
	"""

	number_qubits_used = 0
	qubit_list_per_variable_dict = {}

	# Go through all the variables
	for variable_index in range(0, len(list_of_variables)):

		# Depending on the method, each variable requires 2* (integer qubits + fractional qubits) for method 1 or
		# 1 + (integer qubits + fractional qubits) for method 2
		num_qubits_variable = 0
		if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"]     # Integer part & Positive
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part & Positive
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"]     # Integer part & Negative
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part & Negative

		elif method == LinearCircuitSolver.Method.METHOD_WITH_SIGN:
			num_qubits_variable += 1    # Sign
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"]    # Integer part
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part

		else:

			raise Exception("Method not valid : " + str(method))

		# List of qubits of a single variable with the format q1, q2, etc. Depending on the position of the variable in
		# x vector, an offset has to be added to the index of the first qubit.
		list_of_qubits = []
		for index in range(number_qubits_used, number_qubits_used + num_qubits_variable):
			list_of_qubits.append("q" + str(index + 1))

		# Add the list of qubits to each variable
		qubit_list_per_variable_dict[list_of_variables[variable_index]] = list_of_qubits

		number_qubits_used += num_qubits_variable

	return qubit_list_per_variable_dict, number_qubits_used


def get_value(method, raw_values_dict, num_qubits_dict, list_of_qubits):
	"""
	This function gets the value of each variable from the qubits values returned by the annealer solver
	:param method:
	:param raw_values_dict: response provided by the annealer solver (in raw)
	:param num_qubits_dict: dictionary with number of qubits for integer and fractional parts of each variable
	:param list_of_qubits: list of qubits of each variable
	:return: it returns the converted value, after processing the qubit values.
	"""

	value = 0
	qubit_index = 0
	if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:

		# Get number of qubits Fractional / positive
		for index in range(0, num_qubits_dict["FRACTIONAL"]):

			qubit_name = list_of_qubits[qubit_index]
			value += 1/pow(2, num_qubits_dict["FRACTIONAL"] - index) * raw_values_dict[qubit_name]

			qubit_index += 1

		# Get number of qubits Integer / positive
		for index in range(0, num_qubits_dict["INTEGER"]):
			qubit_name = list_of_qubits[qubit_index]
			value += pow(2, index) * raw_values_dict[qubit_name]

			qubit_index += 1

		# Get number of qubits Fractional / negative
		for index in range(0, num_qubits_dict["FRACTIONAL"]):
			qubit_name = list_of_qubits[qubit_index]
			value -= 1 / pow(2, num_qubits_dict["FRACTIONAL"] - index) * raw_values_dict[qubit_name]

			qubit_index += 1

		# Get number of qubits Integer / negative
		for index in range(0, num_qubits_dict["INTEGER"]):
			qubit_name = list_of_qubits[qubit_index]
			value -= pow(2, index) * raw_values_dict[qubit_name]

			qubit_index += 1

	elif method == LinearCircuitSolver.Method.METHOD_WITH_SIGN:

		# Sign
		qubit_name = list_of_qubits[qubit_index]
		value -= pow(2, num_qubits_dict["INTEGER"]) * raw_values_dict[qubit_name]
		qubit_index += 1

		# fractional part
		for index in range(0, num_qubits_dict["FRACTIONAL"]):

			qubit_name = list_of_qubits[qubit_index]
			value += 1/pow(2, num_qubits_dict["FRACTIONAL"] - index) * raw_values_dict[qubit_name]

			qubit_index += 1

		# Integer part
		for index in range(0, num_qubits_dict["INTEGER"]):
			qubit_name = list_of_qubits[qubit_index]
			value += pow(2, index) * raw_values_dict[qubit_name]

			qubit_index += 1

	else:
		raise Exception("Method not valid : " + str(method))

	return value
