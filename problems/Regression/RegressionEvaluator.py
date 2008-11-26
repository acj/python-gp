import evaluation
import math

class RegressionEvaluator(evaluation.Evaluator):
	"""Regression evaluator"""

	def __init__(self):
		self.program = None

	def Evaluate(self, program):
		"""Evaluate the given program against a known-correct
		Multiplexer.  For this, we utilize published truth tables."""
		self.program = program
		num_of_pts = 100
		total_difference = 0.0	
		curpt = -1.0
		formula = None
		for dx in range(0, num_of_pts + 1):
			# x^2 + x + 1
			formula = curpt*curpt+curpt+1
			dx_difference = abs(formula - self.EvaluateProgramAtPoint(curpt))
			total_difference += dx_difference
			curpt += 2.0/num_of_pts
		return total_difference

	def EvaluateProgramAtPoint(self, input_string):
		"""Evaluate the given input string using this tree-based program.
		If the input string matches, return True; else, return False.  We
		return None if the tree is deemed to be invalid."""
		tree_val = self._SubEvaluate(input_string, 0)
		return tree_val
	
	def _SubEvaluate(self, input_string, index):
		if index <= self.program.max_index:
			node_value = self.program.tree[index].GetValue()
			# Addition
			if node_value == '+':
				return self._SubEvaluate(input_string, 2*index+1) + self._SubEvaluate(input_string, 2*index+2)
			# Subtraction 
			elif node_value == '-':
				return self._SubEvaluate(input_string, 2*index+1) - self._SubEvaluate(input_string, 2*index+2)
			# Multiplication
			elif node_value == '*':
				return self._SubEvaluate(input_string, 2*index+1) * self._SubEvaluate(input_string, 2*index+2)
			# Division
			elif node_value == '/':
				left_val = self._SubEvaluate(input_string, 2*index+1)
				right_val = self._SubEvaluate(input_string, 2*index+2)
				if right_val == 0:
					return 0
				else:
					return left_val/right_val
			# Boolean-valued variables
			elif node_value in ['0','1','2']:
				return float(node_value)
			elif node_value == 'x':
				return float(input_string)
			else:
				print "Bad tree node value: %s" % str(self.program.tree[index].GetValue())
				exit(0)
		print "Access beyond end of tree (index, max_index) = (%d, %d)" % (index, self.program.max_index)
		exit(0)

	def PrintTree(self):
		"""Traverses the tree and prints its structure to the screen"""
		pass
