import evaluation
import math

class RegressionEvaluator(evaluation.Evaluator):
	"""Regression evaluator"""

	def __init__(self):
		pass

	def Evaluate(self, program):
		"""Evaluate the given program against a known-correct
		Multiplexer.  For this, we utilize published truth tables."""
		num_of_pts = 100
		total_difference = 0.0	
		curpt = -1.0
		for dx in range(0, num_of_pts + 1):
			dx_difference = abs((curpt*curpt+curpt+1) - self.EvaluateProgramInstance(program, curpt))
			if dx_difference == None:
				print "Invalid tree detected!"
			#print "|%f - %f| = %f" % (curpt*curpt+curpt+1, self.EvaluateProgramInstance(program, curpt), dx_difference)
			#print "Difference at point %f = %f" % (curpt, dx_difference)
			total_difference += dx_difference
			curpt += 2.0/num_of_pts
		return total_difference

	def EvaluateProgramInstance(self, program, input_string):
		"""Evaluate the given input string using this tree-based program.
		If the input string matches, return True; else, return False.  We
		return None if the tree is deemed to be invalid."""
		tree_val = self._SubEvaluate(program, input_string, 0)
		if program.tree_is_invalid:
			return None
		else:
			return tree_val
	
	def _SubEvaluate(self, program, input_string, index):
		if index <= program.max_index:
			node_value = program.tree[index].GetValue()
			# Addition
			if node_value == '+':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return None
				return self._SubEvaluate(program, input_string, 2*index+1) + self._SubEvaluate(program, input_string, 2*index+2)
			# Subtraction 
			elif node_value == '-':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return None
				return self._SubEvaluate(program, input_string, 2*index+1) - self._SubEvaluate(program, input_string, 2*index+2)
			# Multiplication
			elif node_value == '*':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return None
				return self._SubEvaluate(program, input_string, 2*index+1) * self._SubEvaluate(program, input_string, 2*index+2)
			# Division
			elif node_value == '/':
				if program.tree[2*index+1] == '#' or program.tree[2*index+2] == '#':
					program.tree_is_invalid = True
					return None
				left_val = self._SubEvaluate(program, input_string, 2*index+1)
				right_val = self._SubEvaluate(program, input_string, 2*index+2)
				if right_val == 0:
					return 0
				else:
					return left_val/right_val
			# Boolean-valued variables
			elif node_value in ['-5.0','-4.0','-3.0','-2.0','-1.0','0.0','1.0','2.0','3.0','4.0','5.0']:
				return float(node_value)
			elif node_value == 'x':
				return float(input_string)
			else:
				print "Bad tree node value: %s" % str(program.tree[index].GetValue())
				exit(0)
		print "Access beyond end of tree (index, max_index) = (%d, %d)" % (index, program.max_index)
		exit(0)

	def PrintTree(self):
		"""Traverses the tree and prints its structure to the screen"""
		pass
