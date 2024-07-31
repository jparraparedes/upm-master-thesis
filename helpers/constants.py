#!/usr/bin/env python3

"""
Master's Thesis Quantum Computing in Electronics Design (Universidad Politecnica de Madrid)
Code with constants/associated functions used throughout the code

:author: Javier Parra Paredes
"""


class LinearCircuitSolver:
	"""
	This class defines a set of constants/functions used throughout the code
	"""

	class Method:
		"""
		This class defines the methods used in this code (Method 1/METHOD_WITHOUT_SIGN or Method 2/METHOD_WITH_SIGN)
		"""
		METHOD_WITHOUT_SIGN = "METHOD_WITHOUT_SIGN"     # Same number of qubits for positive and negative part
		METHOD_WITH_SIGN = "METHOD_WITH_SIGN"           # 1 qubit for sign and the rest of qubits for absolute value

	class TestCircuits:
		"""
		This class defines the electronic circuits under test (TEST_CIRCUIT 1 to 4) and associated functions
		"""

		TEST_CIRCUIT_1 = "TEST_CIRCUIT_1"
		TEST_CIRCUIT_2 = "TEST_CIRCUIT_2"
		TEST_CIRCUIT_3 = "TEST_CIRCUIT_3"
		TEST_CIRCUIT_4 = "TEST_CIRCUIT_4"

		@staticmethod
		def get_test_circuit_path(test_circuit):
			"""
			This function returns the file path of the netlist file in SPICE format of the circuit under test
			:param test_circuit: test circuit under test (TestCircuits)
			:return: it returns the path of the netlist file in SPICE format
			"""

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuits\\test_circuit_1\\netlist_test_circuit_1.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuits\\test_circuit_2\\netlist_test_circuit_2.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuits\\test_circuit_3\\netlist_test_circuit_3.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuits\\test_circuit_4\\netlist_test_circuit_4.net',
			}
			return d[test_circuit]

		@staticmethod
		def get_test_circuit_image(test_circuit):
			"""
			This function returns the file name of the schematic file (.png) of the circuit under test
			:param test_circuit: test circuit under test (TestCircuits)
			:return: it returns the name of schematic file in png format
			"""

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuit_1.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuit_2.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuit_3_mna.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuit_4.png',
			}
			return d[test_circuit]

		@staticmethod
		def get_test_circuit_netlist_info(test_circuit):
			"""
			This function returns the file name of the netlist information (.png, provided by LTSpice) of the circuit
			under test
			:param test_circuit: test circuit under test (TestCircuits)
			:return: it returns the name of netlist file in png format
			"""

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuit_1_netlist.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuit_2_netlist.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuit_3_mna_netlist.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuit_4_netlist.png',
			}
			return d[test_circuit]

		@staticmethod
		def get_test_circuit_solution(test_circuit):
			"""
			This function returns the file name of the solution information (.png, provided by LTSpice) of the circuit
			under test
			:param test_circuit: test circuit under test (TestCircuits)
			:return: it returns the name of solution file in png format
			"""

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuit_1_solution.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuit_2_solution.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuit_3_mna_solution.png',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuit_4_solution.png',
			}
			return d[test_circuit]

		@staticmethod
		def get_test_circuit_solution_file(test_circuit):
			"""
			This function returns the file name of the solution information (.txt, provided by LTSpice) of the circuit
			under test. This information is used to compare with obtained results.
			:param test_circuit: test circuit under test (TestCircuits)
			:return: it returns the name of solution file in txt format
			"""

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuit_1_solution.txt',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuit_2_solution.txt',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuit_3_solution.txt',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuit_4_solution.txt',
			}
			return d[test_circuit]


class AnnealerSolution:
	"""
	This class defines the constants used to select the Annealer Solver:
	Available at the time of this work: D-Wave Simulator, Hybrid Solver and QPU, Fujitsu Digital Annealer Simulator
	"""
	DWAVE_SIM = "DWAVE_SIM"
	DWAVE_HYBRID_SOLVER = "DWAVE_HYBRID_SOLVER"
	DWAVE_QPU = "DWAVE_QPU"
	FUJITSU_SIM = "FUJITSU_SIM"
