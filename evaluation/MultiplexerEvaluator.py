import Evaluator
import math

class MultiplexerEvaluator(Evaluator.Evaluator):
	"""Multiplexer evaluator"""

	def __init__(self):
		"""Set up our basic truth tables"""

		# Format: (S, A, B, Z), S = selector bit, Z = output
		self.mux3_tt = (	
					(0,1,1,1),
					(0,1,0,1),
					(0,0,1,0),
					(0,0,0,0),
					(1,1,1,1),
					(1,1,0,0),
					(1,0,1,1),
					(1,0,0,0) )
		# Format: (S0, S1, A, B, C, D, Z), S{0,1} = selector bits, Z = output
		self.mux6_tt = (
					(0,0,0,0,0,0,0),
					(0,0,1,0,0,0,1),
					(0,0,0,1,0,0,0),
					(0,0,1,1,0,0,1),
					(0,0,0,0,1,0,0),
					(0,0,1,0,1,0,1),
					(0,0,0,1,1,0,0),
					(0,0,1,1,1,0,1),
					(0,0,0,0,0,1,0),
					(0,0,1,0,0,1,1),
					(0,0,0,1,0,1,0),
					(0,0,0,0,1,1,0),
					(0,0,1,0,1,1,1),
					(0,0,0,1,1,1,0),
					(0,0,1,1,1,1,1),
					(1,0,0,0,0,0,0),
					(1,0,1,0,0,0,0),
					(1,0,0,1,0,0,1),
					(1,0,1,1,0,0,1),
					(1,0,0,0,1,0,0),
					(1,0,1,0,1,0,0),
					(1,0,0,1,1,0,1),
					(1,0,1,1,1,0,1),
					(1,0,0,0,0,1,0),
					(1,0,1,0,0,1,0),
					(1,0,0,1,0,1,1),
					(1,0,1,1,0,1,1),
					(1,0,0,0,1,1,0),
					(1,0,1,0,1,1,0),
					(1,0,0,1,1,1,1),
					(1,0,1,1,1,1,1),
					(0,1,0,0,0,0,0),
					(0,1,1,0,0,0,0),
					(0,1,0,1,0,0,0),
					(0,1,1,1,0,0,0),
					(0,1,0,0,1,0,1),
					(0,1,1,0,1,0,1),
					(0,1,0,1,1,0,1),
					(0,1,1,1,1,0,1),
					(0,1,0,0,0,1,0),
					(0,1,1,0,0,1,0),
					(0,1,0,1,0,1,0),
					(0,1,1,1,0,1,0),
					(0,1,0,0,1,1,1),
					(0,1,1,0,1,1,1),
					(0,1,0,1,1,1,1),
					(0,1,1,1,1,1,1),
					(1,1,0,0,0,0,0),
					(1,1,1,0,0,0,0),
					(1,1,0,1,0,0,0),
					(1,1,1,1,0,0,0),
					(1,1,0,0,1,0,0),
					(1,1,1,0,1,0,0),
					(1,1,0,1,1,0,0),
					(1,1,1,1,1,0,0),
					(1,1,0,0,0,1,1),
					(1,1,1,0,0,1,1),
					(1,1,0,1,0,1,1),
					(1,1,1,1,0,1,1),
					(1,1,0,0,1,1,1),
					(1,1,1,0,1,1,1),
					(1,1,0,1,1,1,1),
					(1,1,1,1,1,1,1) )

	def Evaluate(self, program):
		"""Evaluate the given program against a known-correct
		Multiplexer.  For this, we utilize published truth tables."""
		if program.free_vars == 2:
			return self.Evaluate3mux(program)
		elif program.free_vars == 4:
			return self.Evaluate6mux(program)
		else:
			print >>sys.stderr, "Number of free variables must be 2 or 4"
			sys.exit(1)

	def Evaluate3mux(self, program):
		correct_count = 0
		for input in self.mux3_tt:
			if program.Evaluate(input[0:3]) == input[3]:
				correct_count += 1

		return (float(correct_count)/len(self.mux3_tt))

	def Evaluate6mux(self, program):
		correct_count = 0
		for input in self.mux6_tt:
			if program.Evaluate(input[0:6]) == input[6]:
				correct_count += 1

		return (float(correct_count)/len(self.mux6_tt))
