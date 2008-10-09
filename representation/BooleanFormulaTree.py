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
		# Initialize a vector of choices
		self.choices = [ str(i) for i in range(0, self.free_vars) ]
		# Include non-terminals
		self.choices.append('A')
		self.choices.append('O')
		self.choices.append('N')

	def GetMaxDepth(self):
		return self.max_depth

	def SetMaxDepth(self, max_depth):
		self.max_depth = max_depth

	def RaiseTree(self):
		"""Raise a random (but valid) tree.  The nodes can be non-terminals 
		`AND', `OR', or `NOR' encoded as `A', `O', and `N' respectively, or 
		terminals `0', `1', ..., `N-1', where N is the number of free variables 
		in the Boolean equation."""
		index = 0
		self.tree = [ '-1' for i in range(0, self.max_size + 1) ]
		self.RaiseSubTree(index)
	
	def RaiseSubTree(self, index):
		if index <= self.max_size:
			r = random.randint(0, len(self.choices)-1)
			if self.choices[r] == 'A' and (2*index+2) <= self.max_size:
				# Use AND
				self.tree[index] = 'A'
				self.RaiseSubTree(2*index + 1)
				self.RaiseSubTree(2*index + 2)
			elif self.choices[r] == 'O' and (2*index+2) <= self.max_size:
				# Use OR
				self.tree[index] = 'O'
				self.RaiseSubTree(2*index + 1)
				self.RaiseSubTree(2*index + 2)
			elif self.choices[r] == 'N' and (2*index+2) <= self.max_size:
				# Use NOT
				self.tree[index] = 'N'
				self.RaiseSubTree(2*index + 1)
			else:
				# Must be a terminal - remember to convert to string.  If we
				# got here because our child indices would be out of bounds,
				# then we need to pick a new random terminal.  Otherwise, use
				# the terminal that is already selected.
				if (2*index+2) > self.max_size:
					self.tree[index] = self.choices[random.randint(0, self.free_vars-1)]
				else:
					self.tree[index] = self.choices[r]
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
				out += self.tree[index]
		else:
			print "Tried to exceed array bounds"

		return out
		
	def Pickle(self):
		"""Return a string representation (pickled form) of ourselves"""
		return self.tree
	
	def Mutate(self, num_mutations, mut_prob):
		"""Perform mutation on the tree according to the given
		parameters (number of mutations and the probability that mutation
		should occur.  Currently, we allow mutations to unused parts of
		the tree and do not prune unreachable branches that occur as a
		result of mutation."""
		for i in range(1, num_mutations+1):
			print random.random()
			if random.random() > mut_prob:
				r = random.randint(0, len(self.tree)-1)
				self.tree[r] = random.choice(self.choices)

	def CrossOver(self, other_prog):
		"""Performs a crossover of this program with the program taken
		as a parameter.  Does a basic check to ensure that the max_depth
		property of this program is not violated."""
		xover_pt = 0
		while True:
			xover_pt = random.randint(1, len(self.tree)-1)
			if xover_pt > len(other_prog.tree):
				# Too high for the other tree's size; try again
				continue
			if self.tree[xover_pt] != -1 and other_prog.tree[xover_pt] != -1:
				break
		point_stack = [xover_pt]
		while len(point_stack) > 0:
			next_point = point_stack.pop()
			if other_prog.tree[next_point] != '-1':
				self.tree[next_point] = other_prog.tree[next_point]
			if (2*next_point + 2) < len(other_prog.tree):
				point_stack.append(2*next_point + 1)
				point_stack.append(2*next_point + 2)
		
		# TODO: Check that we're not going to violate max_depth
