from dadk.BinPol import *
from dadk.QUBOSolverCPU import *
import numpy as np
from qubo_formulation.qubo_formulation import get_qubits_per_variable, get_value


# Print Python code for the run in D-Wave quantum processing unit

def get_fujitsu_solution(total_num_qubits, QM, num_reads=4):

	# # Round QM coeffiencients to maximum 5 decimals
	# QM = np.round(QM,4)

	myPoly = BinPol()

	for i in range(total_num_qubits):
		myPoly.set_term(QM[i][i], (i,))

	for i in range(total_num_qubits - 1):
		for j in range(i + 1, total_num_qubits):
			if QM[i][j] != 0:
				myPoly.set_term(QM[i][j], (i, j))

	solver = QUBOSolverCPU(
		number_iterations=500,  # Total number of iterations per run.
		number_runs=num_reads,  # Number of stochastically independent runs.
		temperature_start=0.01,  # Start temperature of the annealing process.
		temperature_end=0.00001,  # End temperature of the annealing process.
		temperature_mode=0,  # 0, 1, or 2 to define the cooling curve:
		#    0, 'EXPONENTIAL':
		#       reduce temperature by factor (1-temperature_decay) every temperature_interval steps
		#    1, 'INVERSE':
		#       reduce temperature by factor (1-temperature_decay*temperature) every temperature_interval steps
		#    2, 'INVERSE_ROOT':
		#       reduce temperature by factor (1-temperature_decay*temperature^2) every temperature_interval steps
		temperature_interval=1,  # Number of iterations keeping temperature constant.
		offset_increase_rate=1.0,
		# Increase of dynamic offset when no bit selected. Set to 0.0 to switch off dynamic energy feature.
		graphics=GraphicsDetail.ALL,  # Switch on graphics output.
		auto_tuning=AutoTuning.AUTO_SCALING,
		# Following methods for scaling ``qubo`` and determining temperatures are available:
		#    AutoTuning.NOTHING:
		#       no action
		#    AutoTuning.SCALING:
		#       ``scaling_factor`` is multiplied to ``qubo``, ``temperature_start``, ``temperature_end`` and ``offset_increase_rate``.
		#    AutoTuning.AUTO_SCALING:
		#       A maximum scaling factor w.r.t. ``scaling_bit_precision`` is multiplied to ``qubo``, ``temperature_start``, ``temperature_end`` and ``offset_increase_rate``.
		#    AutoTuning.SAMPLING:
		#       ``temperature_start``, ``temperature_end`` and ``offset_increase_rate`` are automatically determined.
		#    AutoTuning.AUTO_SCALING_AND_SAMPLING:
		#       Temperatures and scaling factor are automatically determined and applied.
		scaling_bit_precision=62
		# Maximum ``scaling_bit_precision`` for ``qubo``. Used to define the scaling factor for ``qubo``, ``temperature_start``, ``temperature_end`` and ``offset_increase_rate``.
	)

	solution_list = solver.minimize(myPoly)
	print(KEYWORD_EXECUTION_TIME, solution_list.solver_times.duration_execution)
	print(solution_list)

	return solution_list


def process_fujitsu_results(list_of_variables, method, response, num_qubits_dict):

	qubit_list_per_variable_dict, number_qubits_used = get_qubits_per_variable(list_of_variables=list_of_variables,
	                                                                           method=method,
	                                                                           num_qubits_dict=num_qubits_dict)

	variable_value_dict = {}

	result_index = 1

	for solution in response.solutions:
		raw_values_dict = {}
		for i, qubit_value in zip(range(0, len(solution.configuration)), solution.configuration):
			raw_values_dict['q'+ str(i+1)] = qubit_value
		energy = solution.energy
		num_occurrences = solution.frequency

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

	return variable_value_dict