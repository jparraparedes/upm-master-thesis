import numpy as np


def get_qubo_matrix_approach_1(dimension, qubits_int, qubits_dec, A, b):
	"""
	This function returns the QUBO matrix with the same number of qubits for positive and negative part
	For each variable, 2 * (qubits for integer + qubits for fractional) are required for each variable
	:param dimension: dimension of the equation system (example: 3 independent equations -> dimension=3)
	:param qubits_int: number of qubits (integer part)
	:param qubits_dec: number of qubits (decimal part)
	:param A: A Matrix
	:param b: b vector
	:return: QM (Qubo matrix)
	"""

	QM = np.zeros(( 2 *(qubits_int +qubits_dec ) *dimension, 2* (qubits_int + qubits_dec) * dimension))

	for k in range(dimension):  # k corresponds with the row
		for i in range(dimension):  # i corresponds with the column
			for l in range((-1) * qubits_dec, qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				cef1 = pow(2, 2 * l) * pow(A[k][i], 2)
				cef2 = pow(2, l + 1) * A[k][i] * b[k]

				po1 = 2 * (qubits_dec + qubits_int) * i + l + qubits_dec
				po2 = 2 * (qubits_dec + qubits_int) * i + l + qubits_dec + (qubits_int + qubits_dec)

				QM[po1][po1] = QM[po1][po1] + cef1 - cef2
				QM[po2][po2] = QM[po2][po2] + cef1 + cef2

	for k in range(dimension):
		for i in range(dimension):
			for l1 in range((-1) * qubits_dec, qubits_int - 1, 1):
				for l2 in range(l1 + 1, qubits_int):
					qcef = pow(2, l1 + l2 + 1) * pow(A[k][i], 2)
					po1 = 2 * (qubits_dec + qubits_int) * i + l1 + qubits_dec
					po2 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l2

					po3 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l1 + (qubits_int + qubits_dec)
					po4 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l2 + (qubits_int + qubits_dec)

					QM[po1][po2] = QM[po1][po2] + qcef
					QM[po3][po4] = QM[po3][po4] + qcef

	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):
				for l1 in range((-1) * qubits_dec, qubits_int, 1):
					for l2 in range((-1) * qubits_dec, qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * A[k][i] * A[k][j]
						po1 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l1
						po2 = 2 * (qubits_dec + qubits_int) * j + qubits_dec + l2

						po3 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l1 + (qubits_int + qubits_dec)
						po4 = 2 * (qubits_dec + qubits_int) * j + qubits_dec + l2 + (qubits_int + qubits_dec)

						po5 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l1
						po6 = 2 * (qubits_dec + qubits_int) * j + qubits_dec + l2 + (qubits_int + qubits_dec)

						po7 = 2 * (qubits_dec + qubits_int) * i + qubits_dec + l1 + (qubits_int + qubits_dec)
						po8 = 2 * (qubits_dec + qubits_int) * j + qubits_dec + l2

						QM[po1][po2] = QM[po1][po2] + qcef
						QM[po3][po4] = QM[po3][po4] + qcef
						QM[po5][po6] = QM[po5][po6] - qcef
						QM[po7][po8] = QM[po7][po8] - qcef

	# Print Matrix Q
	print("# Matrix Q is")
	print(QM)

	return QM


def get_qubo_matrix_approach_2(dimension, qubits_int, qubits_dec, A, b):
	"""
	This function returns the QUBO matrix with one qubit reserved for sign (positive/negative), using 2-complement and
	the rest for positive values.
	qubits for integer + qubits for fractional + 1 qubit for the sign are required for each variable
	:param dimension: dimension of the equation system (example: 3 independent equations -> dimension=3)
	:param qubits_int: number of qubits (integer part)
	:param qubits_dec: number of qubits (decimal part)
	:param A: A Matrix
	:param b: b vector
	:return: QM (Qubo matrix)
	"""

	QM = np.zeros(((qubits_int + qubits_dec + 1) * dimension,
	               (qubits_int + qubits_dec + 1) * dimension))  # add only one qubit for the sign

	# For calculating the coefficients, it has been considered -(2^m) * qi- where m=qubits_int, instead of -(2^(m + 1)) * qi-

	# linear terms (diagonal)
	for k in range(dimension):  # k corresponds with the row
		for i in range(dimension):  # i corresponds with the column

			cef1 = A[k][i] * b[k] * pow(2, (qubits_int - 1) + 2)  # Coefficient for qi- (third term)
			cef2 = pow(A[k][i], 2) * pow(2, 2 * (qubits_int - 1) + 2)  # Coefficient for qi- (first term)
			# position of qi-
			po1 = (qubits_dec + qubits_int + 1) * i
			QM[po1][po1] = QM[po1][po1] + cef1 + cef2

			for l in range((-1) * qubits_dec, qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				cef3 = pow(2, 2 * l) * pow(A[k][i], 2)  # Coefficient for qil+ (first term)
				cef4 = pow(2, l + 1) * A[k][i] * b[k]  # Coefficient for qil+ (third term)
				# position of qil+
				po2 = (qubits_dec + qubits_int + 1) * i + l + qubits_dec + 1  # add only one qubit for the sign
				QM[po2][po2] = QM[po2][po2] + cef3 - cef4

	# quadratic terms
	for k in range(dimension):
		for i in range(dimension):
			for l in range((-1) * qubits_dec, qubits_int,
			               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
				qcef = pow(2, l + (qubits_int - 1) + 2) * pow(A[k][i], 2)  # Coefficient for qi-qil+ (first term)
				po1 = (qubits_dec + qubits_int + 1) * i
				po2 = (qubits_dec + qubits_int + 1) * i + l + qubits_dec + 1  # add only one qubit for the sign
				QM[po1][po2] = QM[po1][po2] - qcef

	for k in range(dimension):
		for i in range(dimension):
			for l1 in range((-1) * qubits_dec, qubits_int - 1, 1):
				for l2 in range(l1 + 1, qubits_int, 1):
					qcef = pow(2, l1 + l2 + 1) * pow(A[k][i], 2)  # Coefficient for qil1+qil2+ (first term)
					po1 = (qubits_dec + qubits_int + 1) * i + l1 + qubits_dec + 1  # add only one qubit for the sign
					po2 = (qubits_dec + qubits_int + 1) * i + l2 + qubits_dec + 1  # add only one qubit for the sign

					QM[po1][po2] = QM[po1][po2] + qcef

	for k in range(dimension):
		for i in range(dimension - 1):
			for j in range(i + 1, dimension):

				qcef = pow(2, 2 * (qubits_int - 1) + 3) * A[k][i] * A[k][j]  # Coefficient for qi-qj- (second term)
				po1 = (qubits_dec + qubits_int + 1) * i
				po2 = (qubits_dec + qubits_int + 1) * j
				QM[po1][po2] = QM[po1][po2] + qcef

				for l in range((-1) * qubits_dec, qubits_int,
				               1):  # (l = -qubits_dec ... qubits_int-1). Integer + Float part
					qcef = pow(2, l + (qubits_int - 1) + 2) * A[k][i] * A[k][
						j]  # Coefficient for qi-qjl+ and qj-qil+ (second term)
					po1 = (qubits_dec + qubits_int + 1) * i
					po2 = (qubits_dec + qubits_int + 1) * j + l + qubits_dec + 1  # add only one qubit for the sign
					po3 = (qubits_dec + qubits_int + 1) * j
					po4 = (qubits_dec + qubits_int + 1) * i + l + qubits_dec + 1  # add only one qubit for the sign

					QM[po1][po2] = QM[po1][po2] - qcef

					if po3 - po4 > 0:
						QM[po4][po3] = QM[po4][po3] - qcef
					else:
						QM[po3][po4] = QM[po3][po4] - qcef

				for l1 in range((-1) * qubits_dec, qubits_int, 1):
					for l2 in range((-1) * qubits_dec, qubits_int, 1):
						qcef = pow(2, l1 + l2 + 1) * A[k][i] * A[k][j]  # Coefficient for qil1+qil2+ (second term)

						po1 = (qubits_dec + qubits_int + 1) * i + qubits_dec + l1 + 1  # add only one qubit for the sign
						po2 = (qubits_dec + qubits_int + 1) * j + qubits_dec + l2 + 1  # add only one qubit for the sign

						QM[po1][po2] = QM[po1][po2] + qcef

	# Print Matrix Q
	print("# Matrix Q is")
	print(QM)

	return QM