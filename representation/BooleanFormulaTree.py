import math
import random

class BooleanFormulaTree:
	"""A individual represented by a Boolean Formula Tree"""

	def __init__(self, free_vars, max_depth=5):
		"""We use a dictionary for storage in this representation"""
		self.tree = []
		self.free_vars = free_vars
		self.max_depth = max_depth
		self.max_size = int(math.pow(2, max_depth))

	def GetMaxDepth(self):
		return self.max_depth

	def SetMaxDepth(self, max_depth):
		self.max_depth = max_depth

	def RaiseTree(self):
		"""Raise a random (but valid) tree.  The nodes can be non-terminals 
		`AND', `OR', or `NOR' encoded as `A', `O', and `N' respectively, or 
		terminals `0', `1', ..., `N-1', where N is the number of free variables 
		in the Boolean equation."""

		# Initialize a vector of choices
		choices = [ str(i) for i in range(0, self.free_vars) ]

		# Include non-terminals
		choices.append('A')
		choices.append('O')
		choices.append('N')
		index = 0
		self.tree = [ '-1' for i in range(0, self.max_size + 1) ]

		self.RaiseSubTree(index, choices)
	
	def RaiseSubTree(self, index, choices):
		if index <= self.max_size:
			r = random.randint(0, len(choices)-1)
			if choices[r] == 'A' and (2*index+2) <= self.max_size:
				# Use AND
				self.tree[index] = 'A'
				self.RaiseSubTree(2*index + 1, choices)
				self.RaiseSubTree(2*index + 2, choices)
			elif choices[r] == 'O' and (2*index+2) <= self.max_size:
				# Use OR
				self.tree[index] = 'O'
				self.RaiseSubTree(2*index + 1, choices)
				self.RaiseSubTree(2*index + 2, choices)
			elif choices[r] == 'N' and (2*index+2) <= self.max_size:
				# Use NOT
				self.tree[index] = 'N'
				self.RaiseSubTree(2*index + 1, choices)
			else:
				# Must be a terminal - remember to convert to string.  If we
				# got here because our child indices would be out of bounds,
				# then we need to pick a new random terminal.  Otherwise, use
				# the terminal that is already selected.
				if (2*index+2) > self.max_size:
					self.tree[index] = choices[random.randint(0, self.free_vars-1)]
				else:
					self.tree[index] = choices[r]
		else:
			print "Tried to raise a subtree past the array bounds"
		
	def ToString(self, index=0, out=""):
		if index <= self.max_size: 
			if self.tree[index] == 'A':
				out += "(AND "
				out += self.ToString(2*index+1)
				out += self.ToString(2*index+2)
				out += ")"
			elif self.tree[index] == 'O':
				out += "(OR "
				out += self.ToString(2*index+1)
				out += self.ToString(2*index+2)
				out += ")"
			elif self.tree[index] == 'N':
				out += "(NOT "
				out += self.ToString(2*index+1)
				out += ")"
			else:
				# Must be a terminal
				out += self.tree[index] + " "
		else:
			print "Tried to exceed array bounds"

		return out
		
	def Pickle(self):
		"""Return a string representation (pickled form) of ourselves"""
		return self.tree
