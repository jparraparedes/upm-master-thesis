from qubo_formulation import qubo_formulation
from modified_nodal_analysis.mna_matrix_generator import MnaMatrixGenerator
from helpers.constants import LinearCircuitSolver, AnnealerSolution
from helpers.linear_solver import get_solution, get_results
from fujitsu_tools.fujitsu_tools import TemperatureMode
from dadk.QUBOSolverCPU import *

"""
######################## Input Parameters #############################################################################
"""
test_circuit = LinearCircuitSolver.TestCircuits.get_test_circuit_path(LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1)
method = LinearCircuitSolver.Method.METHOD_WITH_SIGN
annealer_solution = AnnealerSolution.DWAVE_SIM
number_of_integer_qubits = 4
number_of_fractional_qubits = 6

if annealer_solution == AnnealerSolution.FUJITSU_SIM:
    num_reads = 125
else:
    num_reads = 500

# FUJITSU Parameters
fujitsu_number_iterations = 1000
fujitsu_temperature_start = 0.1
fujitsu_temperature_end = 0.000001
fujitsu_temperature_mode = TemperatureMode.EXPONENTIAL
fujitsu_temperature_interval = 1

fujitsu_offset_increase_rate = 0.1
fujitsu_scaling_bit_precision = 62
fujitsu_auto_tuning = AutoTuning.AUTO_SCALING
fujitsu_graphics = GraphicsDetail.ALL

# DWAVE Parameters
dwave_chain_strength = 10
dwave_annealing_time_us = 20

"""
######################## Modified Nodal Analysis ######################################################################
"""
mna_matrix_gen = MnaMatrixGenerator()
z_matrix, x_matrix, a_matrix, df, symbol_value_dict = mna_matrix_gen.get_a_b_x_matrix(netlist_filename=test_circuit)

print(z_matrix)
print(x_matrix)
print(a_matrix)
print(df)
print(symbol_value_dict)
# Establish the number of integer and fractional qubits per each variable
num_qubits_dict = {}
for i in range(0, len(x_matrix)):
    dict_aux = {"INTEGER": number_of_integer_qubits, "FRACTIONAL": number_of_fractional_qubits}
    num_qubits_dict[x_matrix[i]] = dict_aux

A_matrix = np.asarray(a_matrix.subs(symbol_value_dict))
b_matrix = [expr.subs(symbol_value_dict) for expr in z_matrix]

qubit_list_per_variable_dict, number_qubits_used = \
    qubo_formulation.get_qubits_per_variable(list_of_variables=x_matrix, method=method, num_qubits_dict=num_qubits_dict)

# QUBO Matrix is generated
qubo_matrix = qubo_formulation.get_qubo_matrix(method=method, list_of_variables=x_matrix,
                                               num_qubits_dict=num_qubits_dict,
                                               A_matrix=A_matrix, b_matrix=b_matrix)

# QUBO problem is solved by chosen annealer solution
response = get_solution(annealer_solution=annealer_solution, number_qubits_used=number_qubits_used,
                        qubo_matrix=qubo_matrix, num_reads=num_reads,
                        dwave_chain_strength=dwave_chain_strength,
                        dwave_annealing_time_us=dwave_annealing_time_us,
                        fujitsu_number_iterations=fujitsu_number_iterations,
                        fujitsu_temperature_start=fujitsu_temperature_start,
                        fujitsu_temperature_end=fujitsu_temperature_end,
                        fujitsu_temperature_mode=fujitsu_temperature_mode,
                        fujitsu_temperature_interval=fujitsu_temperature_interval,
                        fujitsu_offset_increase_rate=fujitsu_offset_increase_rate,
                        fujitsu_scaling_bit_precision=fujitsu_scaling_bit_precision,
                        fujitsu_auto_tuning=fujitsu_auto_tuning,
                        fujitsu_graphics=fujitsu_graphics)

# Postprocess results
data = get_results(annealer_solution=annealer_solution, x_matrix=x_matrix, method=method, response=response,
                   num_qubits_dict=num_qubits_dict)

# Print data
print(data)

if annealer_solution == AnnealerSolution.FUJITSU_SIM:
    response.display_graphs()
