#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design
Code with functions used with D-Wave solvers (Simulator/Hybrid Solver and QPU)

:author: Javier Parra Paredes
"""

# Import libraries
from dwave.samplers import SimulatedAnnealingSampler
from dwave.system import DWaveSampler, EmbeddingComposite
from dwave.system import LeapHybridSampler
from helpers.variables import get_qubits_per_variable, get_value
from helpers.constants import AnnealerSolution
from dwave.inspector import show
import os

# Import information of D-Wave token (it changes for every user)
with open('dwave_token.txt', 'r') as file:
    os.environ['DWAVE_API_TOKEN'] = file.read()


def get_dwave_solution(annealer_solution, total_num_qubits, qubo_matrix, num_reads=500, chain_strength=100,
                       annealing_time_us=20):
    """
    This function receives the QUBO matrix obtained previously and according to the D-Wave solver (Simulator, Hybrid
    Solver and QPU) and set its configuration (QUBO terms, number of reads, chain strength and annealing time in us)
    :param annealer_solution: annealer solver (Simulator, Hybrid Solver or QPU)
    :param total_num_qubits: total number of qubits used in QUBO matrix
    :param qubo_matrix: QUBO matrix
    :param num_reads: total number of reads (by default, 500) (only for D-Wave Simulator and QPU). For the case of
    Hybrid solver, the number of reads is always 1.
    :param chain_strength: chain strength parameter (only for D-Wave QPU).
    :param annealing_time_us: annealing time in us of each read.
    :return: it returns the response in raw provided by D-Wave solver
    """

    # The terms to program in the annealer solver are split into 2 dictionaries: linear and quadratic terms

    # dictionary with linear terms (diagonal terms of QUBO matrix)
    linear_dict = {}
    for i in range(total_num_qubits - 1):
        linear = i + 1
        linear_dict[("q" + str(linear), "q" + str(linear))] = qubo_matrix[i][i]

    linear_dict[("q" + str(total_num_qubits), "q" + str(total_num_qubits))] = \
        qubo_matrix[total_num_qubits - 1][total_num_qubits - 1]

    # dictionary with quadratic terms (off - upper diagonal terms of QUBO matrix)
    quadratic_dict = {}

    for i in range(total_num_qubits - 1):
        for j in range(i + 1, total_num_qubits):
            if qubo_matrix[i][j] != 0:
                qdrt1 = i + 1
                qdrt2 = j + 1
                quadratic_dict[("q" + str(qdrt1), "q" + str(qdrt2))] = qubo_matrix[i][j]

    # A dictionary is built with linear and quadratic terms
    qubo = dict(linear_dict)
    qubo.update(quadratic_dict)

    # Call to the D-Wave solvers (Simulator, Hybrid Solver or QPU) with the applicable parameters
    if annealer_solution == AnnealerSolution.DWAVE_SIM:
        sampler = SimulatedAnnealingSampler()
        response = sampler.sample_qubo(qubo, num_reads=num_reads)
    elif annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER:
        sampler = LeapHybridSampler()
        response = sampler.sample_qubo(qubo)
    elif annealer_solution == AnnealerSolution.DWAVE_QPU:
        sampler = EmbeddingComposite(DWaveSampler())
        response = sampler.sample_qubo(qubo, num_reads=num_reads, chain_strength=chain_strength,
                                       annealing_time=annealing_time_us)
        # For the case of D-Wave QPU, it shows the D-Wave Inspector (Web format) after providing the solution
        show(response)
    else:
        raise Exception("Annealer Solution not found : {}".format(annealer_solution))

    response = response.aggregate()

    # Print response (raw)
    print(response)

    # Print number of occurrences, values and energy of each provided solution. The handling of the response is
    # different if provided by the simulator/ Hybrid Solver or QPU.
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
    """
    This function processes the response (raw) provided by D-Wave solvers (Simulator, Hybrid Solver or QPU) and rebuilds
    the values of the variables from the qubit values obtained in the response.
    :param annealer_solution: D-Wave solver used (Simulator, Hybrid Solver or QPU). Depending on the solver, the format
    of the response changes.
    :param list_of_variables: list of variables (x vector), in symbolic format
    :param method: method used (method 1 or same number of qubits for integer and fractional parts or method 2 or one
    qubit dedicated to the sign and the rest for the absolute value)
    :param response: response provided by D-Wave solver
    :param num_qubits_dict: information of number of qubits used for integer/fractional part of each variable.
    :return: it returns a dictionary with the processed information of the results, ordered with this format (result_1
    is the minimum energy solution obtained:
    Example:
    {'result_1': {V1: 3, V2: 1, I_V1: -2, 'occurrences': 73, 'energy': -9.0},
    'result_2': {V1: 3, V2: 1, I_V1: -1, 'occurrences': 23, 'energy': -8.0}, etc

    """

    qubit_list_per_variable_dict, number_qubits_used = get_qubits_per_variable(list_of_variables=list_of_variables,
                                                                               method=method,
                                                                               num_qubits_dict=num_qubits_dict)

    variable_value_dict = {}
    result_index = 1

    if annealer_solution == AnnealerSolution.DWAVE_SIM or annealer_solution == AnnealerSolution.DWAVE_HYBRID_SOLVER:
        # In the case of D-Wave Simulator and Hybrid Solver, the data is returned with this format and order:
        # Values of qubits, energy and number of occurrences of each solution
        for raw_values_dict, energy, num_occurrences in response.data():
            # For each result returned by dwave, calculate the variable values

            result_dict = {}

            # For each variable, it calls to a function "get_value" which rebuilds the value of the variable. This
            # function requires the method used (method 1 or 2), raw values dictionary (qubits values), number of qubits
            # of each variable used (integer and fractional parts) and assignment of qubits per each variable.
            for variable_index in range(0, len(list_of_variables)):
                result_dict[list_of_variables[variable_index]] = \
                    get_value(method, raw_values_dict, num_qubits_dict[list_of_variables[variable_index]],
                              qubit_list_per_variable_dict[list_of_variables[variable_index]])

            result_dict["occurrences"] = num_occurrences
            result_dict["energy"] = energy

            variable_value_dict["result_" + str(result_index)] = result_dict
            result_index += 1

    elif annealer_solution == AnnealerSolution.DWAVE_QPU:
        # In the case of D-Wave QPU, the data is returned with this format and order:
        # Values of qubits, energy and number of occurrences, and other parameters (not used) of each solution
        for raw_values_dict, energy, num_occurrences, _ in response.data():
            # For each variable, it calls to a function "get_value" which rebuilds the value of the variable. This
            # function requires the method used (method 1 or 2), raw values dictionary (qubits values), number of qubits
            # of each variable used (integer and fractional parts) and assignment of qubits per each variable.

            result_dict = {}

            for variable_index in range(0, len(list_of_variables)):
                result_dict[list_of_variables[variable_index]] = \
                    get_value(method, raw_values_dict, num_qubits_dict[list_of_variables[variable_index]],
                              qubit_list_per_variable_dict[list_of_variables[variable_index]])

            result_dict["occurrences"] = num_occurrences
            result_dict["energy"] = energy

            variable_value_dict["result_" + str(result_index)] = result_dict
            result_index += 1
    else:
        raise Exception("Annealer solution not found : {}".format(annealer_solution))

    # A dictionary with the results already converted is returned (see format in the description of the function above)
    return variable_value_dict
