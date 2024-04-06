import numpy as np
import matplotlib.pyplot as plt
from helpers.constants import LinearCircuitSolver


def get_qubo_matrix(method, list_of_variables, num_qubits_dict, A_matrix, b_matrix):

	if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:
		qubo_matrix = get_qubo_matrix_without_sign_method(list_of_variables, num_qubits_dict, A_matrix, b_matrix)
	elif method == LinearCircuitSolver.Method.METHOD_WITH_SIGN:
		qubo_matrix = get_qubo_matrix_with_sign_method(list_of_variables, num_qubits_dict, A_matrix, b_matrix)
	else:
		raise Exception("method not valid {}".format(method))

	return qubo_matrix

def get_qubo_matrix_without_sign_method(list_of_variables, num_qubits_dict, A_matrix, b_matrix):
	"""
	This function returns the QUBO matrix with the same number of qubits for positive and negative part
	For each variable, 2 * (qubits for integer + qubits for fractional) are required for each variable
	:param list_of_variables:
	:param num_qubits_dict:
	:param A_matrix: A Matrix
	:param b_matrix: b vector
	:return: QM (Qubo matrix)
	"""
	dimension = len(list_of_variables)
	total_num_qubits = 0

	# Calculate the number of rows and columns of QUBO matrix (square matrix), which is really the total number of qubits
	for variable in list_of_variables:
		total_num_qubits += 2 * (num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"])

	# Create QUBO matrix (square matrix) with all the elements initialized to 0
	QM = np.zeros(( total_num_qubits, total_num_qubits))

	for k in range(dimension):  # k corresponds with the row (from 0 to dimension -1). Matrix is handled from index=0
		for i in range(dimension):  # i corresponds with the column (from 0 to dimension -1). Matrix is handled from index=0

			# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l in range((-1) * num_qubits_fract, num_qubits_int, 1):  # (l = -qubits_fract ... qubits_int-1).
				# Integer + Float part
				cef1 = pow(2, 2 * l) * pow(A_matrix[k][i], 2)   # First term, lineal one
				cef2 = pow(2, l + 1) * A_matrix[k][i] * b_matrix[k] # Third term, lineal one

				# Position in the QUBO matrix is given by the variable position (i), total number of qubits and the
				# qubit position
				# Relative qubit position is given by l + num_qubits_fract, where l=-qubits_fract ... qubits_int-1
				po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l + num_qubits_fract)    # Positive part
				# Relative qubit position in the negative part is given by l + num_qubits_fract + (num_qubits_int +
				# num_qubits_fract) to add the positions of the positive part
				po2 = 2 * (num_qubits_fract + num_qubits_int) * i + (l + num_qubits_fract) + (num_qubits_int +
				                                                                            num_qubits_fract)  # Negative part

				QM[po1][po1] = QM[po1][po1] + cef1 - cef2   # Positive part
				QM[po2][po2] = QM[po2][po2] + cef1 + cef2   # Negative part

	# first term (quadratic term)
	for k in range(dimension):
		for i in range(dimension):
			# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l1 in range((-1) * num_qubits_fract, num_qubits_int -1, 1):
				for l2 in range(l1 + 1, num_qubits_int):
					qcef = pow(2, l1 + l2 + 1) * pow(A_matrix[k][i], 2)
					po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
					po2 = 2 * (num_qubits_fract + num_qubits_int) * i + (l2 + num_qubits_fract)

					po3 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
					po4 = 2 * (num_qubits_fract + num_qubits_int) * i + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

					QM[po1][po2] = QM[po1][po2] + qcef
					QM[po3][po4] = QM[po3][po4] + qcef

	# second term (all quadratic terms)
	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):
				# Number of integer and fractional qubits per each variable is given by num_qubits_dict (parameter)
				num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
				num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

				for l1 in range((-1) * num_qubits_fract, num_qubits_int, 1):
					for l2 in range((-1) * num_qubits_fract, num_qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * A_matrix[k][i] * A_matrix[k][j]
						po1 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
						po2 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract)

						po3 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
						po4 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

						po5 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract)
						po6 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)

						po7 = 2 * (num_qubits_fract + num_qubits_int) * i + (l1 + num_qubits_fract) + (num_qubits_int + num_qubits_fract)
						po8 = 2 * (num_qubits_fract + num_qubits_int) * j + (l2 + num_qubits_fract)

						QM[po1][po2] = QM[po1][po2] + qcef
						QM[po3][po4] = QM[po3][po4] + qcef
						QM[po5][po6] = QM[po5][po6] - qcef
						QM[po7][po8] = QM[po7][po8] - qcef

	# Print Matrix Q
	print("# Matrix Q is")
	print(QM)

	return QM

def get_qubo_matrix_with_sign_method(list_of_variables, num_qubits_dict, A_matrix, b_matrix):
	"""
	This function returns the QUBO matrix with one qubit reserved for sign (positive/negative), using 2-complement and
	the rest for positive values.
	qubits for integer + qubits for fractional + 1 qubit for the sign are required for each variable
	:param dimension: dimension of the equation system (example: 3 independent equations -> dimension=3)
	:param num_qubits_int: number of qubits (integer part)
	:param num_qubits_dec: number of qubits (decimal part)
	:param A_matrix: A Matrix
	:param b_matrix: b vector
	:return: QM (Qubo matrix)
	"""

	dimension = len(list_of_variables)
	# Get total number of qubits
	num_rows = 0
	num_columns = 0
	for variable in list_of_variables:
		num_rows += num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"] + 1
		num_columns += num_qubits_dict[variable]["INTEGER"] + num_qubits_dict[variable]["FRACTIONAL"] + 1

	QM = np.zeros((num_rows, num_columns))  # add only one qubit for the sign

	# For calculating the coefficients, it has been considered -(2^m) * qi- where m=qubits_int, instead of -(2^(m + 1)) * qi-

	# linear terms (diagonal)
	for k in range(dimension):  # k corresponds with the row
		for i in range(dimension):  # i corresponds with the column

			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			cef1 = A_matrix[k][i] * b_matrix[k] * pow(2, (num_qubits_int - 1) + 2)  # Coefficient for qi- (third term)
			cef2 = pow(A_matrix[k][i], 2) * pow(2, 2 * (num_qubits_int - 1) + 2)  # Coefficient for qi- (first term)
			# position of qi-
			po1 = (num_qubits_fract + num_qubits_int + 1) * i
			QM[po1][po1] = QM[po1][po1] + cef1 + cef2

			for l in range((-1) * num_qubits_fract, num_qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				cef3 = pow(2, 2 * l) * pow(A_matrix[k][i], 2)  # Coefficient for qil+ (first term)
				cef4 = pow(2, l + 1) * A_matrix[k][i] * b_matrix[k]  # Coefficient for qil+ (third term)
				# position of qil+
				po2 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign
				QM[po2][po2] = QM[po2][po2] + cef3 - cef4

	# quadratic terms
	for k in range(dimension):
		for i in range(dimension):
			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l in range((-1) * num_qubits_fract, num_qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				qcef = pow(2, l + (num_qubits_int - 1) + 2) * pow(A_matrix[k][i], 2)  # Coefficient for qi-qil+ (first term)
				po1 = (num_qubits_fract + num_qubits_int + 1) * i
				po2 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign
				QM[po1][po2] = QM[po1][po2] - qcef

	for k in range(dimension):
		for i in range(dimension):

			# Get number of qubits (integer and float) for the specific variable
			num_qubits_int = num_qubits_dict[list_of_variables[dimension - 1]]["INTEGER"]
			num_qubits_fract = num_qubits_dict[list_of_variables[dimension - 1]]["FRACTIONAL"]

			for l1 in range((-1) * num_qubits_fract, num_qubits_int - 1, 1):
				for l2 in range(l1 + 1, num_qubits_int, 1):
					qcef = pow(2, l1 + l2 + 1) * pow(A_matrix[k][i], 2)  # Coefficient for qil1+qil2+ (first term)
					po1 = (num_qubits_fract + num_qubits_int + 1) * i + l1 + num_qubits_fract + 1  # add only one qubit for the sign
					po2 = (num_qubits_fract + num_qubits_int + 1) * i + l2 + num_qubits_fract + 1  # add only one qubit for the sign

					QM[po1][po2] = QM[po1][po2] + qcef

	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):

				# Get number of qubits (integer and float) for the specific variable
				num_qubits_int = num_qubits_dict[list_of_variables[dimension-1]]["INTEGER"]
				num_qubits_fract = num_qubits_dict[list_of_variables[dimension-1]]["FRACTIONAL"]

				qcef = pow(2, 2 * (num_qubits_int - 1) + 3) * A_matrix[k][i] * A_matrix[k][j]  # Coefficient for qi-qj- (second term)
				po1 = (num_qubits_fract + num_qubits_int + 1) * i
				po2 = (num_qubits_fract + num_qubits_int + 1) * j
				QM[po1][po2] = QM[po1][po2] + qcef

				for l in range((-1) * num_qubits_fract, num_qubits_int,
				               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
					qcef = pow(2, l + (num_qubits_int - 1) + 2) * A_matrix[k][i] * A_matrix[k][
						j]  # Coefficient for qi-qjl+ and qj-qil+ (second term)
					po1 = (num_qubits_fract + num_qubits_int + 1) * i
					po2 = (num_qubits_fract + num_qubits_int + 1) * j + l + num_qubits_fract + 1  # add only one qubit for the sign
					po3 = (num_qubits_fract + num_qubits_int + 1) * j
					po4 = (num_qubits_fract + num_qubits_int + 1) * i + l + num_qubits_fract + 1  # add only one qubit for the sign

					QM[po1][po2] = QM[po1][po2] - qcef

					if po3 - po4 > 0:
						QM[po4][po3] = QM[po4][po3] - qcef
					else:
						QM[po3][po4] = QM[po3][po4] - qcef

				for l1 in range((-1) * num_qubits_fract, num_qubits_int, 1):
					for l2 in range((-1) * num_qubits_fract, num_qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * A_matrix[k][i] * A_matrix[k][j]  # Coefficient for qil1+qil2+ (second term)

						po1 = (num_qubits_fract + num_qubits_int + 1) * i + num_qubits_fract + l1 + 1  # add only one qubit for the sign
						po2 = (num_qubits_fract + num_qubits_int + 1) * j + num_qubits_fract + l2 + 1  # add only one qubit for the sign

						QM[po1][po2] = QM[po1][po2] + qcef

	# Print Matrix Q
	print("# Matrix Q is")
	print(QM)

	return QM


def get_qubits_per_variable(list_of_variables, method, num_qubits_dict):

	number_qubits_used = 0
	qubit_list_per_variable_dict = {}

	for variable_index in range(0, len(list_of_variables)):

		num_qubits_variable = 0
		if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"]     # Integer part & Positive
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part & Positive
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"]     # Integer part & Negative
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part & Negative

		elif method == LinearCircuitSolver.Method.METHOD_WITH_SIGN:
			num_qubits_variable += 1    # Sign
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["INTEGER"] # Integer part
			num_qubits_variable += num_qubits_dict[list_of_variables[variable_index]]["FRACTIONAL"]  # Fractional part

		else:

			raise Exception("Method not valid : " + str(method))

		list_of_qubits = []
		for index in range(number_qubits_used, number_qubits_used + num_qubits_variable):
			list_of_qubits.append("q" + str(index + 1))

		qubit_list_per_variable_dict[list_of_variables[variable_index]] = list_of_qubits

		number_qubits_used += num_qubits_variable

	return qubit_list_per_variable_dict, number_qubits_used


def get_value(method, raw_values_dict, num_qubits_dict, list_of_qubits):

	value = 0
	qubit_index = 0
	if method == LinearCircuitSolver.Method.METHOD_WITHOUT_SIGN:

		# Get number of qubits Fractional / positive
		for index in range(0, num_qubits_dict["FRACTIONAL"]):

			qubit_name = list_of_qubits[qubit_index]
			value += 1/pow(2, num_qubits_dict["FRACTIONAL"] - index) * raw_values_dict[qubit_name]

			qubit_index +=1

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

			qubit_index +=1

		# Integer part
		for index in range(0, num_qubits_dict["INTEGER"]):
			qubit_name = list_of_qubits[qubit_index]
			value += pow(2, index) * raw_values_dict[qubit_name]

			qubit_index += 1

	else:
		raise Exception("Method not valid : " + str(method))

	return value

def plot_histogram(data):

	result_dict = {}

	for result in data.keys():

		for variable_name in data[result].keys():

			if variable_name != 'occurrences' and variable_name != 'energy':
				if variable_name not in result_dict.keys(): # variable already in the dictionary, update the value/occurrences
					result_dict[variable_name] = {'list_of_values': [], 'list_of_occurrences': []}

				value = data[result][variable_name]
				occurrences = data[result]['occurrences']

				# Check if value in list
				list_of_values = result_dict[variable_name]['list_of_values']
				if value in list_of_values:

					# get position on the list (index)
					index = list_of_values.index(value)
					# update number of occurrences
					list_of_occurrences = result_dict[variable_name]['list_of_occurrences']
					list_of_occurrences[index] = occurrences + list_of_occurrences[index]
					result_dict[variable_name]['list_of_occurrences'] = list_of_occurrences
				else:
					list_of_values = result_dict[variable_name]['list_of_values']
					list_of_values.append(value)
					result_dict[variable_name]['list_of_values'] = list_of_values
					list_of_occurrences = result_dict[variable_name]['list_of_occurrences']
					list_of_occurrences.append(occurrences)
					result_dict[variable_name]['list_of_occurrences'] = list_of_occurrences

	fig, axs = plt.subplots(1, len(result_dict.keys()), sharey=True, tight_layout=True)

	# We can set the number of bins with the *bins* keyword argument.
	index = 0
	for variable_name in result_dict.keys():
		axs[index].bar(result_dict[variable_name]['list_of_values'], result_dict[variable_name]['list_of_occurrences'],
		               width=0.01)
		axs[index].set_xlabel(str(variable_name))
		index += 1

	plt.show()

	return result_dict

# def add_weights(qubo_matrix, list_of_variables, list_of_values):
#
#
# 	for i in range(0, len(qubo_matrix[0])):
# 		qubo_matrix[i][0] = qubo_matrix[i][0] * 100
#
# 	for i in range(0, len(qubo_matrix[0])):
# 		qubo_matrix[i][2] = qubo_matrix[i][2] * 100
# 	# qubo_matrix[2][2] = qubo_matrix[2][2] * 100
#
# 	for i in range(0, len(qubo_matrix[0])):
# 		qubo_matrix[i][13] = qubo_matrix[i][13] * 100
#
# 	# for variable, i in list_of_variables, range(0, len(list_of_variables)):
# 	# 	value = list_of_values[i]
# 	# 	# Find the coefficients in the QUBO matrix of the variable.
# 	return qubo_matrix