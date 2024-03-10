import numpy as np
from qubo_formulation import qubo_formulation
from modified_nodal_analysis.mna_matrix_generator import MnaMatrixGenerator
from dwave_tools import dwave_tools

test_circuit = 'test_circuits\\test_circuit_1\\netlist_test_circuit_1.net'
# test_circuit = 'test_circuits\\test_circuit_2\\netlist_test_circuit_2.net'
# test_circuit = 'test_circuits\\test_circuit_4\\netlist_test_circuit_4.net'
method = qubo_formulation.Method.METHOD_WITH_SIGN
simulated = True
num_reads = 500

mna_matrix_gen = MnaMatrixGenerator()
z_matrix, x_matrix, a_matrix, df, symbol_value_dict = mna_matrix_gen.get_a_b_x_matrix(netlist_filename=test_circuit)

print(z_matrix)
print(x_matrix)
print(a_matrix)
print(df)
print(symbol_value_dict)

dimension = len(x_matrix)

num_qubits_dict = {
	x_matrix[0]: {"INTEGER": 2, "FRACTIONAL": 2},
	x_matrix[1]: {"INTEGER": 2, "FRACTIONAL": 2},
	x_matrix[2]: {"INTEGER": 2, "FRACTIONAL": 2}
}

# num_qubits_dict = {
# 	x_matrix[0]: {"INTEGER": 2, "FRACTIONAL": 1},
# 	x_matrix[1]: {"INTEGER": 3, "FRACTIONAL": 1},
# 	x_matrix[2]: {"INTEGER": 4, "FRACTIONAL": 2},
# 	x_matrix[3]: {"INTEGER": 3, "FRACTIONAL": 2},
# 	x_matrix[4]: {"INTEGER": 2, "FRACTIONAL": 1},
# 	x_matrix[5]: {"INTEGER": 2, "FRACTIONAL": 3},
# 	x_matrix[6]: {"INTEGER": 3, "FRACTIONAL": 1},
# 	x_matrix[7]: {"INTEGER": 5, "FRACTIONAL": 2},
# 	x_matrix[8]: {"INTEGER": 3, "FRACTIONAL": 1}
# }

# num_qubits_dict = {
# 	x_matrix[0]: {"INTEGER": 2, "FRACTIONAL": 1},
# 	x_matrix[1]: {"INTEGER": 3, "FRACTIONAL": 1},
# 	x_matrix[2]: {"INTEGER": 4, "FRACTIONAL": 2},
# 	x_matrix[3]: {"INTEGER": 3, "FRACTIONAL": 2},
# 	x_matrix[4]: {"INTEGER": 2, "FRACTIONAL": 1},
# 	x_matrix[5]: {"INTEGER": 2, "FRACTIONAL": 3},
# 	x_matrix[6]: {"INTEGER": 3, "FRACTIONAL": 1},
# 	x_matrix[7]: {"INTEGER": 5, "FRACTIONAL": 2},
# 	x_matrix[8]: {"INTEGER": 3, "FRACTIONAL": 1}
# }


print(a_matrix)
A_matrix = np.asarray(a_matrix.subs(symbol_value_dict))
b_matrix = [expr.subs(symbol_value_dict) for expr in z_matrix]

qubit_list_per_variable_dict, number_qubits_used = \
	qubo_formulation.get_qubits_per_variable(list_of_variables=x_matrix,
	                                         method=method,
	                                         num_qubits_dict=num_qubits_dict)

if method == qubo_formulation.Method.METHOD_WITHOUT_SIGN:
	qubo_matrix = qubo_formulation.get_qubo_matrix_approach_1_optimized_num_qubits(list_of_variables=x_matrix,
	                                                                               num_qubits_dict=num_qubits_dict,
	                                                                               A_matrix=A_matrix,
	                                                                               b_matrix=b_matrix)

	response = dwave_tools.get_dwave_solution_approach_1(total_num_qubits=number_qubits_used,
	                                                     QM=qubo_matrix, num_reads=num_reads, simulated=simulated)

elif method == qubo_formulation.Method.METHOD_WITH_SIGN:
	qubo_matrix = qubo_formulation.get_qubo_matrix_approach_2_optimized_num_qubits(list_of_variables=x_matrix,
	                                                                               num_qubits_dict=num_qubits_dict,
	                                                                               A_matrix=A_matrix,
	                                                                               b_matrix=b_matrix)

	response = dwave_tools.get_dwave_solution_approach_2(total_num_qubits=number_qubits_used,
	                                                     QM=qubo_matrix, num_reads=num_reads, simulated=simulated)
else:
	raise Exception("Method not recognized : " + method)

data = qubo_formulation.process_dwave_results(list_of_variables=x_matrix, method=method, response=response,
                                              num_qubits_dict=num_qubits_dict, simulated=simulated)

print(data)

print(qubo_formulation.plot_histogram(data))
