import math
import random
import sets

class Tree:
	"""A representation for a tree-based organism"""

	def __init__(self, max_depth, nodeset):
		"""We use a dictionary for storage in this representation"""
		self.tree = []
		#self.free_vars = free_vars
		#self.select_vars = int(math.log(self.free_vars, 2))
		self.max_depth = max_depth
		self.max_index = int(math.pow(2, max_depth)) - 1
		self.tree_is_invalid = False

		# Initialize a vector of node choices
		self.nodeset = nodeset

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
		self.tree = [ '#' for i in range(0, self.max_index + 1) ]
		self.tree[0] = random.choice(self.nodeset.GetNonterminals())
		self.RaiseSubTree(2*index+1)
		self.RaiseSubTree(2*index+2)
	
	def RaiseSubTree(self, index):
		if index <= self.max_index:
			r = random.randint(0, len(self.nodeset.nodes)-1)
			if self.nodeset.nodes[r].GetArity() == 2 and (2*index+2) <= self.max_index:
				# Use AND
				self.tree[index] = self.nodeset.nodes[r]
				self.RaiseSubTree(2*index + 1)
				self.RaiseSubTree(2*index + 2)
			elif self.nodeset.nodes[r].GetArity() == 1 and (2*index+2) <= self.max_index:
				self.tree[index] = self.nodeset.nodes[r]
				self.RaiseSubTree(2*index + 1)
			else:
				# Must be a terminal - remember to convert to string.  If we
				# got here because our child indices would be out of bounds,
				# then we need to pick a new random terminal.  Otherwise, use
				# the terminal that is already selected.
				if (2*index+2) > self.max_index:
					self.tree[index] = random.choice(self.nodeset.GetTerminals())
				else:
					self.tree[index] = self.nodeset.nodes[r]
		else:
			print "Tried to raise a subtree past the array bounds"
		
	def ToString(self, index=0, out=""):
		if index <= self.max_index and self.tree[index] != '#': 
			if self.tree[index].GetArity() == 2:
				out += "(" + self.tree[index].GetName() + " "
				out += self.ToString(2*index+1)
				out += self.ToString(2*index+2)
				out += ")"
			elif self.tree[index].GetArity() == 1:
				out += "(" + self.tree[index].GetName() + " "
				out += self.ToString(2*index+1)
				out += ")"
			else:
				# Must be a terminal
				out += self.tree[index].GetName()

		return out
		
	def Pickle(self):
		"""Return a string representation (pickled form) of ourselves"""
		return self.tree
	
	def Mutate(self, num_mutations, mut_prob):
		"""Perform mutation on the tree according to the given
		parameters (number of mutations and the probability that
		mutation should occur.	Currently, we do not prune unreachable
		branches that occur as a result of mutation."""

		r = 0
		for i in range(1, num_mutations+1):
			if random.random() < mut_prob:
				while True:
					r = random.randint(0, len(self.tree)-1)
					if self.tree[r] != '#':
						# Do a sanity check on the arity of the node that we're
						# replacing.
						if self.tree[r].IsTerminal(): 
							self.tree[r] = random.choice(self.nodeset.GetTerminals())
						else:
							# Preserve node arity
							self.tree[r] = random.choice(self.nodeset.GetNodesByArity(self.tree[r].GetArity()))

						# Exit the loop - we mutated a node
						break

	def CrossOver(self, other_prog, xo_prob):
		"""Performs a crossover of this program with the program and a
		probability taken as parameters.  Does a basic check to ensure
		that the max_depth property of this program is not violated."""

		# Skip the crossover with probability (1 - xo_prob)
		if random.random() >= xo_prob:
			return

		# Find the indices of valid (i.e., not '#') entities in both 
		# trees.  Compute the intersection of these two sets.  Choose 
		# one set member at random to be the crossover point.
		eligible_points_tree1 = list(index for index,item in enumerate(self.tree) if item != '#')
		eligible_points_tree2 = list(index for index,item in enumerate(other_prog.tree) if item != '#')

		set_tree1 = sets.Set(eligible_points_tree1)
		set_tree2 = sets.Set(eligible_points_tree2)
		eligible_points = set_tree1.intersection(set_tree2)

		eligible_points_list = list(eligible_points)

		xover_pt_self = None
		xover_pt_other = None
		# Create a strong bias (90%) for functions over leaves
		while True:
			xover_pt_self = random.choice(eligible_points_list)
			#print "First point: %d" % xover_pt_self
			if self.tree[xover_pt_self] not in self.nodeset.GetNonterminals():
				if random.random() < 0.1:
					break
			else:
				break
		while True:
			xover_pt_other = random.choice(eligible_points_list)
			#print "Second point: %d" % xover_pt_self
			if other_prog.tree[xover_pt_other] not in self.nodeset.GetNonterminals():
				if random.random() < 0.1:
					break
			else:
				break

		point_stack = [xover_pt_other]
		# Mind the index offset between the two trees
		xover_diff = xover_pt_self - xover_pt_other

		while len(point_stack) > 0:
			next_point = point_stack.pop()
			# Stopping case: reading a '#'
			if other_prog.tree[next_point] != '#':
				if ((2 * next_point + 2) + xover_diff) <= self.max_index and ((2 * next_point + 2) <= other_prog.max_index):
					self.tree[next_point + xover_diff] = other_prog.tree[next_point]
					point_stack.append(2*next_point + 1)
					point_stack.append(2*next_point + 2)
				else:
					# TODO: Need to do something better here.  Verify
					# the tree depth before doing crossover?
					self.tree[next_point + xover_diff] = str(random.choice(self.nodeset.GetTerminals()))
		
		# TODO: Check that we're not going to violate max_depth
