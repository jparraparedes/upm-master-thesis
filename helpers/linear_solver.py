
from fujitsu_tools import fujitsu_tools
from dwave_tools import dwave_tools
from helpers.constants import AnnealerSolution

def get_solution(annealer_solution, number_qubits_used, qubo_matrix, num_reads,
                 dwave_chain_strength=None,
                 fujitsu_number_iterations=None, fujitsu_temperature_start=None, fujitsu_temperature_end=None,
                 fujitsu_temperature_mode=None, fujitsu_temperature_interval=None, fujitsu_offset_increase_rate=None,
                 fujitsu_scaling_bit_precision=None, fujitsu_auto_tuning=None, fujitsu_graphics=None):

	if annealer_solution == AnnealerSolution.FUJITSU_SIM or annealer_solution == AnnealerSolution.FUJITSU_DIG_ANNEALER:
		response = fujitsu_tools.get_fujitsu_solution(annealer_solution=annealer_solution,
		                                              total_num_qubits=number_qubits_used, QM=qubo_matrix,
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
		                                          total_num_qubits=number_qubits_used, QM=qubo_matrix,
		                                          num_reads=num_reads, chain_strength=dwave_chain_strength)
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