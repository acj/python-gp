import representation

class TreeProgram(representation.BooleanFormulaTree):
	"""A representation of GP programs that uses a tree structure."""

	def __init__(self):
		representation.BooleanFormulaTree.__init__(self, 2)
		pass

	def Evaluate(self, input_string):
		if self._SubEvaluate(input_string, 0):
			return True
		else:
			return False
	
	def _SubEvaluate(self, input_string, index):
		if index <= self.max_size:
			if self.tree[index] == 'A':
				if self._SubEvaluate(input_string, 2*index+1) and self._SubEvaluate(input_string, 2*index+2):
					return True
				else:
					return False
			elif self.tree[index] == 'O':
				if self._SubEvaluate(input_string, 2*index+1) or self._SubEvaluate(input_string, 2*index+2):
					return True
				else:
					return False
			elif self.tree[index] == 'N':
				if not self._SubEvaluate(input_string, 2*index+1):
					return True
				else:
					return False
			else:
				if input_string[int(self.tree[index])] == 1:
					return True
				else:
					return False

	def PrintTree(self):
		"""Traverses the tree and prints its structure to the screen"""
		pass
