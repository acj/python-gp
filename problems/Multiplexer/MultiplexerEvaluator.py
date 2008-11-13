import evaluation
import math

class MultiplexerEvaluator(evaluation.Evaluator):
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
		return self.Evaluate6mux(program)

	def Evaluate6mux(self, program):
		correct_count = 0
		for input in self.mux6_tt:
			result = self.EvaluateProgramInstance(program, input[0:6])
			if result == input[6]:
				correct_count += 1
			elif result == None:
				# Invalid tree - return a fitness of 0.0
				#print "*** INVALID TREE ***"
				return 0.0	

		return (float(correct_count)/len(self.mux6_tt))
	
	def EvaluateProgramInstance(self, program, input_string):
		"""Evaluate the given input string using this tree-based program.
		If the input string matches, return True; else, return False.  We
		return None if the tree is deemed to be invalid."""
		if program.tree_is_invalid:
			return None

		if self._SubEvaluate(program, input_string, 0):
			return True
		else:
			return False
	
	def _SubEvaluate(self, program, input_string, index):
		if index <= program.max_index:
			node_value = program.tree[index].GetValue()
			# AND
			if node_value == 'A':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return False
				if self._SubEvaluate(program, input_string, 2*index+1) and self._SubEvaluate(program, input_string, 2*index+2):
					return True
				else:
					return False
			# OR
			elif node_value == 'O':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return False
				if self._SubEvaluate(program, input_string, 2*index+1) or self._SubEvaluate(program, input_string, 2*index+2):
					return True
				else:
					return False
			# NOT
			elif node_value == 'N':
				if program.tree[2*index+1] == '#':
					program.tree_is_invalid = True
					return False
				if not self._SubEvaluate(program, input_string, 2*index+1):
					return True
				else:
					return False
			# Boolean-valued variables
			elif node_value in ['0','1','2','3','4','5']:
				if input_string[int(node_value)] == 1:
					return True
				elif input_string[int(node_value)] == 0:
					return False
				else:
					print >>sys.stderr, "Invalid tree element: `%s'" % input_string[int(program.tree[index])]
					program.tree_is_invalid = True
					return False
			else:
				print "Bad tree node value: %s" % str(program.tree[index].GetValue())
				exit(0)

	def PrintTree(self):
		"""Traverses the tree and prints its structure to the screen"""
		pass
