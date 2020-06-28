# importing Qiskit
from qiskit import IBMQ, BasicAer, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram

from pytket import Circuit
from pytket.qiskit import tk_to_qiskit

def simulate(circuit, shots=1024, x="0", verbose=False):
	"""simulates circuit with given input

	Args:
	    circuit (QuantumCircuit): Circuit to be simualted
	    shots (int, optional): number of shots to simulate
	    x (str, optional): input string
	    verbose (bool, optional): prints extra output

	Returns:
	    TYPE: dictionary of simulation
	"""
	if type(circuit) == Circuit: #is a tket circuit
		return simulate(tk_to_qiskit(circuit), shots=shots, x=x, verbose=verbose) #converts to qiskit
	names = []
	regs = []
	for q in circuit.qubits:
		name = q.register.name
		size = len(q.register)
		if name not in names:
			names.append(name)
			regs.append(size)

	if verbose: print(names, regs)

	#assuming that we only have 2: control + anciallary
	qra = QuantumRegister(regs[0], name=names[0])
	if len(regs) > 1:
		qran = QuantumRegister(regs[1], name=names[1])
		qa = QuantumCircuit(qra,qran)
	else:
		qa = QuantumCircuit(qra)

	if len(x) != sum(regs): x += "0" * (sum(regs) - len(x))
	if verbose: print(x)
	for bit in range(len(x)):
		if verbose: print(x[bit], type(x[bit]))
		if x[bit] != "0":
			qa.x(bit)
	qa.barrier()

	qa.extend(circuit)

	if verbose:
		print(qa)

	"""backend_sim = Aer.get_backend('statevector_simulator')
				job_sim = execute(qa, backend_sim)
				statevec = job_sim.result().get_statevector()"""

	backend = BasicAer.get_backend('qasm_simulator')
	results = execute(qa, backend=backend, shots=shots).result()
	answer = results.get_counts()
	return answer

def validate(circuit, expected, verbose=False):
    """Checks all possible inputs for a circuit and ensures that only values in expected == 1

    Args:
        circuit (QuantumCircuit): circuit to be evaluated
        bits (int): number of qubits in put
        expected ([str]): inputs which should give 1 as ouput, e.g ['001', '100', etc.]
        verbose (bool, optional): prints extra output
    """
    if verbose: print("one day make it for long ones it just does random selection because even for 10 this is FAT. Also this will help future rl implemenations")

    if len(expected) == 0: raise ValueError("len(expected) == 0 - currently assuming there is one correct answer")
    bits = len(expected[0])
    form = "0" + str(bits) + "b"
    for i in range(2**bits):
    	x = format(i,form)
    	ans = simulate(circuit,x=x,shots=1)
    	val = int(max(ans, key = ans.get))
    	if verbose: print(x , "=" , val)
    	if val and x not in expected or not val and x in expected: print("wrong answer for" , x)

    print("all finished")
