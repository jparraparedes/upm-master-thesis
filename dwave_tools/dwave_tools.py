from dwave.samplers import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave.system import LeapHybridSampler
from qubo_formulation.qubo_formulation import get_qubits_per_variable, get_value
from helpers.constants import AnnealerSolution

import os

with open('dwave_token.txt', 'r') as file:
    os.environ['DWAVE_API_TOKEN'] = file.read()

# Print Python code for the run in D-Wave quantum processing unit

def get_dwave_solution(annealer_solution, total_num_qubits, QM, num_reads=500):

	linear_dict = {}
	for i in range(total_num_qubits - 1):
		linear = i + 1
		linear_dict[("q" + str(linear), "q" + str(linear))] = QM[i][i]

	linear_dict[
		("q" + str(total_num_qubits), "q" + str(total_num_qubits))] = \
	QM[total_num_qubits - 1][total_num_qubits - 1]

	quadratic_dict = {}

	for i in range(total_num_qubits - 1):
		for j in range(i + 1, total_num_qubits):
			if QM[i][j] != 0:
				qdrt1 = i + 1
				qdrt2 = j + 1
				quadratic_dict[("q" + str(qdrt1), "q" + str(qdrt2))] = QM[i][j]

	qubo = dict(linear_dict)
	qubo.update(quadratic_dict)

	if annealer_solution == AnnealerSolution.DWAVE_SIM:
		sampler = SimulatedAnnealingSampler()
		response = sampler.sample_qubo(qubo, num_reads=num_reads)
	elif annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER:
		sampler = LeapHybridSampler()
		response = sampler.sample_qubo(qubo)
	elif annealer_solution == AnnealerSolution.DWAVE_QPU:
		sampler = EmbeddingComposite(DWaveSampler())
		response = sampler.sample_qubo(qubo, num_reads=num_reads, chain_strength=100)
	else:
		raise Exception("Annealer Solution not found : {}".format(annealer_solution))

	response = response.aggregate()

	print(response)

	if annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER:
		for values, energy, num_occurrences in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {} energy'.format(num_occurrences, num_reads, variables, energy))
	elif annealer_solution == AnnealerSolution.DWAVE_QPU:
		for values, energy, num_occurrences, _ in response.data():
			variables = [key for key in values if values[key] != 0]
			print('{:4.0f}/{} occurrences: {} energy: {}'.format(num_occurrences, num_reads, variables, energy))
	else:
		raise Exception("Annealer Solution not found : {}".format(annealer_solution))

	return response

def process_dwave_results(annealer_solution, list_of_variables, method, response, num_qubits_dict):

	qubit_list_per_variable_dict, number_qubits_used = get_qubits_per_variable(list_of_variables=list_of_variables, method=method,
	                                                       num_qubits_dict=num_qubits_dict)

	variable_value_dict = {}
	result_index = 1

	if annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER:
		for raw_values_dict, energy, num_occurrences in response.data():
			# For each result returned by dwave, calculate the variable values

			result_dict = {}

			for variable_index in range(0, len(list_of_variables)):
				result_dict[list_of_variables[variable_index]] = get_value(method, raw_values_dict,
				                                    num_qubits_dict[list_of_variables[variable_index]],
				                                    qubit_list_per_variable_dict[list_of_variables[variable_index]])

			result_dict["occurrences"] = num_occurrences
			result_dict["energy"] = energy

			variable_value_dict["result_" + str(result_index)] = result_dict
			result_index += 1

	elif annealer_solution == AnnealerSolution.DWAVE_QPU:
		for raw_values_dict, energy, num_occurrences, _ in response.data():
			# For each result returned by dwave, calculate the variable values

			result_dict = {}

			for variable_index in range(0, len(list_of_variables)):
				result_dict[list_of_variables[variable_index]] = get_value(method, raw_values_dict,
				                                                           num_qubits_dict[
					                                                           list_of_variables[variable_index]],
				                                                           qubit_list_per_variable_dict[
					                                                           list_of_variables[variable_index]])

			result_dict["occurrences"] = num_occurrences
			result_dict["energy"] = energy

			variable_value_dict["result_" + str(result_index)] = result_dict
			result_index += 1
	else:
		raise Exception("Annealer solution not found : {}".format(annealer_solution))

	return variable_value_dict