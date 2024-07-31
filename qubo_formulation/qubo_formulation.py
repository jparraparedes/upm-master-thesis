#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design (Universidad Politecnica de Madrid)
Code with QUBO problem formulation. The system of linear equations is provided as input (Modified Nodal Analysis) and
QUBO matrix is the output of the functions shown below.

:author: Javier Parra Paredes

QUBO formulation is based on:

Reference : QUBO formulations for numerical quantum computing.
Author: Kyungtaek Juna,
Research Center, Innovative Quantum Computed Tomography, Seoul, Republic of Korea
ktfriends@gmail.com
https://arxiv.org/abs/2106.10819

"""

# Import Libraries
import numpy as np
from helpers.constants import LinearCircuitSolver


def get_qubo_matrix(method, list_of_variables, num_qubits_dict, a_matrix, b_matrix):
	"""
	this function builds the QUBO matrix according to the selected method
	:param method: Method 1 or same number of qubits for positive and negative values, Method 2 or one qubit for the
	sign and the rest of qubits for absolute value
	:param list_of_variables: list of variables in symbolic format (x matrix)
	:param num_qubits_dict: dictionary with the number of qubits for integer and fractional parts of each variable.
	Currently, the same number of qubits for all variables
	:param a_matrix: A matrix returned by Modified Nodal Analysis
	:param b_matrix: b matrix (constants) returned by Modified Nodal Analysis
	:return: QUBO matrix
	"""

	if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:
		qubo_matrix = get_qubo_matrix_without_sign_method(list_of_variables, num_qubits_dict, a_matrix, b_matrix)
	elif method == LinearCircuitSolver.Method.METHOD_WITH_SIGN:
		qubo_matrix = get_qubo_matrix_with_sign_method(list_of_variables, num_qubits_dict, a_matrix, b_matrix)
	else:
		raise Exception("method not valid {}".format(method))

	return qubo_matrix


def get_qubo_matrix_without_sign_method(list_of_variables, num_qubits_dict, a_matrix, b_matrix):
	"""
	This function returns the QUBO matrix with the same number of qubits for positive and negative part
	For each variable, 2 * (qubits for integer + qubits for fractional) are required for each variable
	:param list_of_variables: list of variables in symbolic format (x matrix)
	:param num_qubits_dict: dictionary with the number of qubits for integer and fractional parts of each variable.
	Currently, the same number of qubits for all variables
	:param a_matrix: A matrix returned by Modified Nodal Analysis
	:param b_matrix: b matrix (constants) returned by Modified Nodal Analysis
	:return: Qubo matrix
	"""
	dimension = len(list_of_variables)
	total_num_qubits = 0

	# Calculate the number of rows and columns of QUBO matrix (square matrix), which is really the total number of
	# qubits of all the variables
	for variable in list_of_variables:
		total_num_qubits += 2 * (num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"])

	# Create QUBO matrix (square matrix) with all the elements initialized to 0
	qubo_matrix = np.zeros((total_num_qubits, total_num_qubits))

	for k in range(dimension):  # k corresponds with the row (from 0 to dimension -1). Matrix is handled from index=0
		for i in range(dimension):  # i corresponds with the column (from 0 to dimension -1). Matrix is handled from # index=0

			# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l in range((-1) * num_qubits_fract, num_qubits_int, 1):  # (l = -qubits_fract ... qubits_int-1).
				# Integer + Float part
				cef1 = pow(2, 2 * l) * pow(a_matrix[k][i], 2)   # First term, lineal one
				cef2 = pow(2, l + 1) * a_matrix[k][i] * b_matrix[k]     # Third term, lineal one

				# Position in the QUBO matrix is given by the variable position (i), total number of qubits and the
				# qubit position
				# Relative qubit position is given by l + num_qubits_fract, where l=-qubits_fract ... qubits_int-1
				po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l + num_qubits_fract)    # Positive part
				# Relative qubit position in the negative part is given by l + num_qubits_fract + (num_qubits_int +
				# num_qubits_fract) to add the positions of the positive part
				po2 = 2 * (num_qubits_fract + num_qubits_int) * i + (l + num_qubits_fract) + \
				      (num_qubits_int + num_qubits_fract)  # Negative part

				qubo_matrix[po1][po1] = qubo_matrix[po1][po1] + cef1 - cef2   # Positive part
				qubo_matrix[po2][po2] = qubo_matrix[po2][po2] + cef1 + cef2   # Negative part

	# first term (quadratic term)
	for k in range(dimension):
		for i in range(dimension):
			# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l1 in range((-1) * num_qubits_fract, num_qubits_int - 1, 1):
				for l2 in range(l1 + 1, num_qubits_int):
					qcef = pow(2, l1 + l2 + 1) * pow(a_matrix[k][i], 2)
					po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
					po2 = 2 * (num_qubits_fract + num_qubits_int) * i + (l2 + num_qubits_fract)

					po3 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
					po4 = 2 * (num_qubits_fract + num_qubits_int) * i + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

					qubo_matrix[po1][po2] = qubo_matrix[po1][po2] + qcef
					qubo_matrix[po3][po4] = qubo_matrix[po3][po4] + qcef

	# second term (all quadratic terms)
	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):
				# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
				num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
				num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

				for l1 in range((-1) * num_qubits_fract, num_qubits_int, 1):
					for l2 in range((-1) * num_qubits_fract, num_qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * a_matrix[k][i] * a_matrix[k][j]
						po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
						po2 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract)

						po3 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
						po4 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

						po5 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
						po6 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

						po7 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
						po8 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract)

						qubo_matrix[po1][po2] = qubo_matrix[po1][po2] + qcef
						qubo_matrix[po3][po4] = qubo_matrix[po3][po4] + qcef
						qubo_matrix[po5][po6] = qubo_matrix[po5][po6] - qcef
						qubo_matrix[po7][po8] = qubo_matrix[po7][po8] - qcef

	# Print Matrix Q
	print("# QUBO Matrix Q is:")
	print(qubo_matrix)

	return qubo_matrix


def get_qubo_matrix_with_sign_method(list_of_variables, num_qubits_dict, a_matrix, b_matrix):
	"""
	This function returns the QUBO matrix with one qubit reserved for sign (positive/negative), using 2-complement and
	the rest for absolute values.
	qubits for integer + qubits for fractional + 1 qubit for the sign are required for each variable
	:param list_of_variables: list of variables in symbolic format (x matrix)
	:param num_qubits_dict: dictionary with the number of qubits for integer and fractional parts of each variable.
	Currently, the same number of qubits for all variables
	:param a_matrix: A matrix returned by Modified Nodal Analysis
	:param b_matrix: b matrix (constants) returned by Modified Nodal Analysis
	:return: Qubo matrix
	"""

	dimension = len(list_of_variables)
	# Get total number of qubits
	num_rows = 0
	num_columns = 0
	for variable in list_of_variables:
		num_rows += num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"] + 1
		num_columns += num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"] + 1

	# Create QUBO matrix (square matrix) with all the elements initialized to 0
	qubo_matrix = np.zeros((num_rows, num_columns))  # add only one qubit for the sign

	# For calculating the coefficients, it has been considered -(2^m) * qi- where m=qubits_int,
	# instead of -(2^(m + 1)) * qi-

	# linear terms (diagonal)
	for k in range(dimension):  # k corresponds with the row
		for i in range(dimension):  # i corresponds with the column

			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			cef1 = a_matrix[k][i] * b_matrix[k] * pow(2, (num_qubits_int - 1) + 2)  # Coefficient for qi- (third term)
			cef2 = pow(a_matrix[k][i], 2) * pow(2, 2 * (num_qubits_int - 1) + 2)  # Coefficient for qi- (first term)
			# position of qi-
			po1 = (num_qubits_fract + num_qubits_int + 1) * i
			qubo_matrix[po1][po1] = qubo_matrix[po1][po1] + cef1 + cef2

			for l in range((-1) * num_qubits_fract, num_qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				cef3 = pow(2, 2 * l) * pow(a_matrix[k][i], 2)  # Coefficient for qil+ (first term)
				cef4 = pow(2, l + 1) * a_matrix[k][i] * b_matrix[k]  # Coefficient for qil+ (third term)
				# position of qil+
				po2 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign
				qubo_matrix[po2][po2] = qubo_matrix[po2][po2] + cef3 - cef4

	# quadratic terms
	for k in range(dimension):
		for i in range(dimension):
			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l in range((-1) * num_qubits_fract, num_qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				qcef = pow(2, l + (num_qubits_int - 1) + 2) * pow(a_matrix[k][i], 2)  # Coefficient for qi-qil+ (first term)
				po1 = (num_qubits_fract + num_qubits_int + 1) * i
				po2 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign
				qubo_matrix[po1][po2] = qubo_matrix[po1][po2] - qcef

	for k in range(dimension):
		for i in range(dimension):

			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l1 in range((-1) * num_qubits_fract, num_qubits_int - 1, 1):
				for l2 in range(l1 + 1, num_qubits_int, 1):
					qcef = pow(2, l1 + l2 + 1) * pow(a_matrix[k][i], 2)  # Coefficient for qil1+qil2+ (first term)
					po1 = (num_qubits_fract + num_qubits_int + 1) * i + l1 + num_qubits_fract + 1  # add only one qubit for the sign
					po2 = (num_qubits_fract + num_qubits_int + 1) * i + l2 + num_qubits_fract + 1  # add only one qubit for the sign

					qubo_matrix[po1][po2] = qubo_matrix[po1][po2] + qcef

	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):

				# Get number of qubits (integer and float) for the specific variable
				num_qubits_int = num_qubits_dict[list_of_variables[dimension-1]]["INTEGER"]
				num_qubits_fract = num_qubits_dict[list_of_variables[dimension-1]]["FRACTIONAL"]

				qcef = pow(2, 2 * (num_qubits_int - 1) + 3) * a_matrix[k][i] * a_matrix[k][j]  # Coefficient for qi-qj- # (second term)
				po1 = (num_qubits_fract + num_qubits_int + 1) * i
				po2 = (num_qubits_fract + num_qubits_int + 1) * j
				qubo_matrix[po1][po2] = qubo_matrix[po1][po2] + qcef

				for l in range((-1) * num_qubits_fract, num_qubits_int,
				               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
					qcef = pow(2, l + (num_qubits_int - 1) + 2) * a_matrix[k][i] * a_matrix[k][
						j]  # Coefficient for qi-qjl+ and qj-qil+ (second term)
					po1 = (num_qubits_fract + num_qubits_int + 1) * i
					po2 = (num_qubits_fract + num_qubits_int + 1) * j + l + num_qubits_fract + 1  # add only one qubit for the sign
					po3 = (num_qubits_fract + num_qubits_int + 1) * j
					po4 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign

					qubo_matrix[po1][po2] = qubo_matrix[po1][po2] - qcef

					if po3 - po4 > 0:
						qubo_matrix[po4][po3] = qubo_matrix[po4][po3] - qcef
					else:
						qubo_matrix[po3][po4] = qubo_matrix[po3][po4] - qcef

				for l1 in range((-1) * num_qubits_fract, num_qubits_int, 1):
					for l2 in range((-1) * num_qubits_fract, num_qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * a_matrix[k][i] * a_matrix[k][j]  # Coefficient for qil1+qil2+ (second term)

						po1 = (num_qubits_fract + num_qubits_int + 1) * i + num_qubits_fract + l1 + 1  # add only one qubit for the sign
						po2 = (num_qubits_fract + num_qubits_int + 1) * j + num_qubits_fract + l2 + 1  # add only one qubit for the sign

						qubo_matrix[po1][po2] = qubo_matrix[po1][po2] + qcef

	# Print Matrix Q
	print("# Matrix Q is")
	print(qubo_matrix)

	return qubo_matrix



