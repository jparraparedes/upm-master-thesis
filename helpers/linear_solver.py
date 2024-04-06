
from fujitsu_tools import fujitsu_tools
from dwave_tools import dwave_tools
from helpers.constants import AnnealerSolution

def get_solution(annealer_solution, number_qubits_used, qubo_matrix, num_reads):

	if annealer_solution == AnnealerSolution.FUJITSU_SIM or annealer_solution == AnnealerSolution.FUJITSU_DIG_ANNEALER:
		response = fujitsu_tools.get_fujitsu_solution(total_num_qubits=number_qubits_used, QM=qubo_matrix,
		                                              num_reads=num_reads)
	elif annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER or \
		annealer_solution == AnnealerSolution.DWAVE_QPU:
		response = dwave_tools.get_dwave_solution(annealer_solution=annealer_solution,
		                                          total_num_qubits=number_qubits_used, QM=qubo_matrix,
		                                          num_reads=num_reads)
	else:
		raise Exception("Annealer Solution not found : {}".format(annealer_solution))

	return response

def get_results(annealer_solution, x_matrix, method, response, num_qubits_dict):


	if annealer_solution == AnnealerSolution.FUJITSU_SIM or annealer_solution == AnnealerSolution.FUJITSU_DIG_ANNEALER:
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