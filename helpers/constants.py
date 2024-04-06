
class LinearCircuitSolver:

	class Method:
		METHOD_WITHOUT_SIGN = "METHOD_WITHOUT_SIGN" # Same number of qubits for positive and negative part)
		METHOD_WITH_SIGN = "METHOD_WITH_SIGN"       # 1 qubit for sign and the rest of qubits for (integer/fractional part)

	class TestCircuits:

		TEST_CIRCUIT_1 = "TEST_CIRCUIT_1"
		TEST_CIRCUIT_2 = "TEST_CIRCUIT_2"
		TEST_CIRCUIT_3 = "TEST_CIRCUIT_3"
		TEST_CIRCUIT_4 = "TEST_CIRCUIT_4"
		TEST_CIRCUIT_5 = "TEST_CIRCUIT_5"

		@staticmethod
		def get_test_circuit_path(test_circuit):

			d = {
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_1: 'test_circuits\\test_circuit_1\\netlist_test_circuit_1.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_2: 'test_circuits\\test_circuit_2\\netlist_test_circuit_2.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_3: 'test_circuits\\test_circuit_3\\netlist_test_circuit_3.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_4: 'test_circuits\\test_circuit_4\\netlist_test_circuit_4.net',
				LinearCircuitSolver.TestCircuits.TEST_CIRCUIT_5: 'test_circuits\\test_circuit_5\\netlist_test_circuit_5.net',
			}
			return d[test_circuit]

class AnnealerSolution:

	DWAVE_SIM = "DWAVE_SIM"
	DWAVE_HYBRID_SOLVER = "WAVE_HYBRID_SOLVER"
	DWAVE_QPU = "DWAVE_QPU"

	FUJITSU_SIM = "FUJITSU_SIM"
	FUJITSU_DIG_ANNEALER = "FUJITSU_DIG_ANNEALER"