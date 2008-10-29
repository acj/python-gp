import representation

class TreeProgram(representation.BooleanFormulaTree):
	"""A representation of GP programs that uses a tree structure."""

	def __init__(self):
		representation.BooleanFormulaTree.__init__(self, 4)
		self.tree_is_invalid = False

	def Evaluate(self, input_string):
		"""Evaluate the given input string using this tree-based program.
		If the input string matches, return True; else, return False.  We
		return None if the tree is deemed to be invalid."""
		if self.tree_is_invalid:
			return None

		if self._SubEvaluate(input_string, 0):
			return True
		else:
			return False
	
	def _SubEvaluate(self, input_string, index):
		if index <= self.max_index:
			# AND
			if self.tree[index] == 'A':
				if self.tree[2*index+1] == '#' or self.tree[2*index+2] == '#':
					self.tree_is_invalid = True
					return False
				if self._SubEvaluate(input_string, 2*index+1) and self._SubEvaluate(input_string, 2*index+2):
					return True
				else:
					return False
			# OR
			elif self.tree[index] == 'O':
				if self.tree[2*index+1] == '#' or self.tree[2*index+2] == '#':
					self.tree_is_invalid = True
					return False
				if self._SubEvaluate(input_string, 2*index+1) or self._SubEvaluate(input_string, 2*index+2):
					return True
				else:
					return False
			# NOT
			elif self.tree[index] == 'N':
				if self.tree[2*index+1] == '#':
					self.tree_is_invalid = True
					return False
				if not self._SubEvaluate(input_string, 2*index+1):
					return True
				else:
					return False
			# Boolean-valued variables
			else:
				if input_string[int(self.tree[index])] == 1:
					return True
				elif input_string[int(self.tree[index])] == 0:
					return False
				else:
					print >>sys.stderr, "Invalid tree element: `%s'" % input_string[int(self.tree[index])]
					self.tree_is_invalid = True
					return False

	def PrintTree(self):
		"""Traverses the tree and prints its structure to the screen"""
		pass
