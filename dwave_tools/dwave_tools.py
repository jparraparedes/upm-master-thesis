from dwave.samplers import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite
import os

with open('dwave_token.txt', 'r') as file:
    os.environ['DWAVE_API_TOKEN'] = file.read()

# Print Python code for the run in D-Wave quantum processing unit

def get_dwave_solution_approach_1(total_num_qubits, QM, num_reads=500, simulated=True):
	QM = 1000 * QM  # All coefficients of QM shall be integer

	linear_dict = {}
	for i in range(total_num_qubits - 1):
		linear = i + 1
		linear_dict[("q" + str(linear), "q" + str(linear))] = QM[i][i]

	linear_dict[
		("q" + str(total_num_qubits), "q" + str(total_num_qubits))] = \
	QM[total_num_qubits - 1][total_num_qubits - 1]

	# print(linear_dict)

	quadratic_dict = {}

	for i in range(total_num_qubits - 1):
		for j in range(i + 1, total_num_qubits):
			if QM[i][j] != 0:
				qdrt1 = i + 1
				qdrt2 = j + 1
				quadratic_dict[("q" + str(qdrt1), "q" + str(qdrt2))] = QM[i][j]

	# print(quadratic_dict)

	qubo = dict(linear_dict)
	qubo.update(quadratic_dict)

	# print(qubo)

	if simulated:
		sampler = SimulatedAnnealingSampler()
	else:
		sampler = EmbeddingComposite(DWaveSampler())

	response = sampler.sample_qubo(qubo, num_reads=num_reads)
	response = response.aggregate()

	print(response)

	if simulated:
		for values, energy, num_occurrences in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {}'.format(num_occurrences, num_reads, variables))
	else:
		for values, energy, num_occurrences, _ in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {}'.format(num_occurrences, num_reads, variables))

	return response


# Print Python code for the run in D-Wave quantum processing unit

def get_dwave_solution_approach_2(total_num_qubits, QM, num_reads=500, simulated=True):

	QM = 1000 * QM  # All coefficients of QM shall be integer

	linear_dict = {}
	for i in range(total_num_qubits - 1):
		linear = i + 1
		linear_dict[("q" + str(linear), "q" + str(linear))] = QM[i][i]

	linear_dict[
		("q" + str(total_num_qubits), "q" + str(total_num_qubits))] = \
	QM[total_num_qubits - 1][total_num_qubits - 1]

	# print(linear_dict)

	quadratic_dict = {}

	for i in range(total_num_qubits - 1):
		for j in range(i + 1, total_num_qubits):
			if QM[i][j] != 0:
				qdrt1 = i + 1
				qdrt2 = j + 1
				quadratic_dict[("q" + str(qdrt1), "q" + str(qdrt2))] = QM[i][j]

	qubo = dict(linear_dict)
	qubo.update(quadratic_dict)

	print(qubo)

	if simulated:
		sampler = SimulatedAnnealingSampler()
	else:
		sampler = EmbeddingComposite(DWaveSampler())

	response = sampler.sample_qubo(qubo, num_reads=num_reads)
	response = response.aggregate()

	print(response)

	if simulated:
		for values, energy, num_occurrences in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {}'.format(num_occurrences, num_reads, variables))
	else:
		for values, energy, num_occurrences, _ in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {}'.format(num_occurrences, num_reads, variables))

	return response
