import math
import random
import sets

class Tree:
	"""A representation for a tree-based organism"""

	def __init__(self, max_depth, nodeset):
		"""We use a dictionary for storage in this representation"""
		self.tree = []
		self.max_depth = max_depth
		self.max_index = int(math.pow(2, max_depth)) - 1
		self.tree_is_invalid = False

		# Initialize a vector of node choices
		self.nodeset = nodeset

	def GetMaxDepth(self):
		return self.max_depth

	def SetMaxDepth(self, max_depth):
		self.max_depth = max_depth

	def RaiseTree(self, full=False):
		"""Raise a random (but valid) tree.  The nodes can be non-terminals 
		`AND', `OR', or `NOR' encoded as `A', `O', and `N' respectively, or 
		terminals `0', `1', ..., `N-1', where N is the number of free variables 
		in the Boolean equation."""
		index = 0
		self.tree = [ '#' for i in range(0, self.max_index + 1) ]
		self.tree[0] = random.choice(self.nodeset.GetNonterminals())
		self.RaiseSubTree(2*index+1, full)
		self.RaiseSubTree(2*index+2, full)
	
	def RaiseSubTree(self, index, full):
		if index <= self.max_index:
			node = None
			if full:
				node = random.choice(self.nodeset.GetNonterminals())	
			else:
				r = random.randint(0, len(self.nodeset.nodes)-1)
				node = self.nodeset.nodes[r]
			if node.GetArity() == 2 and (2*index+2) <= self.max_index:
				# Use AND
				self.tree[index] = node
				self.RaiseSubTree(2*index + 1, full)
				self.RaiseSubTree(2*index + 2, full)
			elif node.GetArity() == 1 and (2*index+2) <= self.max_index:
				self.tree[index] = node
				self.RaiseSubTree(2*index + 1, full)
			else:
				# Must be a terminal - remember to convert to string.  If we
				# got here because our child indices would be out of bounds,
				# then we need to pick a new random terminal.  Otherwise, use
				# the terminal that is already selected.
				if (2*index+2) > self.max_index:
					self.tree[index] = random.choice(self.nodeset.GetTerminals())
				else:
					self.tree[index] = node
		else:
			print "Tried to raise a subtree past the array bounds"
		
	def ToString(self, index=0, out=""):
		if len(self.tree) == 0:
			return "()"
		if index <= self.max_index and self.tree[index] != '#': 
			if self.tree[index].GetArity() == 2:
				out += "(" + self.tree[index].GetValue() + " "
				if index != 0:
					out += "\n"
					for n in range(0, int(math.ceil(math.log(2*index+1, 2))) + 1):
						out += "  "
				else:
					out += "\n  "
				out += self.ToString(2*index+1)
				if index != 0:
					out += "\n"
					for n in range(0, int(math.ceil(math.log(2*index+2, 2))) + 1):
						out += "  "
				else:
					out += "\n  "
				out += self.ToString(2*index+2)
				out += ")"
			elif self.tree[index].GetArity() == 1:
				out += "(" + self.tree[index].GetValue() + " "
				if index != 0:
					out += "\n"
					for n in range(0, int(math.ceil(math.log(2*index+1, 2))) + 1):
						out += "  "
				else:
					out += "\n  "
				out += self.ToString(2*index+1)
				out += ")"
			else:
				# Must be a terminal
				out += self.tree[index].GetValue() + " "

		return out
		
	def Pickle(self):
		"""Return a string representation (pickled form) of ourselves"""
		out = "["
		for node in self.tree:
			if node != '#':
				out += node.GetName() + ","
		out += "]"
		return out

	def BriefPickle(self):
		"""Return a string representation (pickled form) of ourselves"""
		out = []
		for node in self.tree:
			if node != '#':
				out.append(node.value)
			else:
				out.append('#')
		return ''.join(out)
	
	def Mutate(self):
		"""Perform mutation on the tree according to the given
		parameters (number of mutations and the probability that
		mutation should occur."""

		r = 0
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

	def CrossOver(self, other_prog, xover_pt=None):
		"""Performs a crossover of this program with the another
		program taken as a parameter.  Does a basic check to
		ensure that the max_depth property of this program is
		not violated."""

		if xover_pt == None:
			# Find the indices of valid (i.e., not '#') entities in both 
			# trees.  Compute the intersection of these two sets.  Choose 
			# one set member at random to be the crossover point.
			eligible_points_tree1 = list(index for index,item in enumerate(self.tree) if item != '#')
			eligible_points_tree2 = list(index for index,item in enumerate(other_prog.tree) if item != '#')

			set_tree1 = sets.Set(eligible_points_tree1)
			set_tree2 = sets.Set(eligible_points_tree2)
			eligible_points = set_tree1.intersection(set_tree2)

			eligible_points_list = list(eligible_points)

			if len(eligible_points_list) == 0:
				print "No eligible points for crossover"
				print self.ToString()
				print other_prog.ToString()
				print "Tree1 candidates: %s" % list(set_tree1)
				print "Tree2 candidates: %s" % list(set_tree2)
			
			# Create a strong bias (90%) for functions over leaves
			while True:
				xover_pt = random.choice(eligible_points_list)
				
				if not self.tree[xover_pt].IsTerminal():
					if random.random() < 0.9:
						break
				else:
					# Terminals
					if random.random() <= 0.1:
						break

		# Temporary copy of this object's tree so that the other program gets
		# nodes from the original (unmodified) tree
		temp_tree = list(self.tree)

		point_stack = [xover_pt]
		while len(point_stack) > 0:
			next_point = point_stack.pop()
			# Stopping case: reading a '#'
			if other_prog.tree[next_point] != '#':
				next_pt_is_term = other_prog.tree[next_point].IsTerminal()
				if (2*next_point+2) <= self.max_index and not next_pt_is_term:
					self.tree[next_point] = other_prog.tree[next_point]
					point_stack.append(2*next_point + 1)
					point_stack.append(2*next_point + 2)
				elif next_pt_is_term:
					# Branch stopping case: terminal node
					self.tree[next_point] = other_prog.tree[next_point]
				else:
					# Bad news: non-terminal read, but we're out of space in
					# the tree.  Pick a random terminal and stop this branch.
					self.tree[next_point] = random.choice(self.nodeset.GetTerminals())

		point_stack = [xover_pt]
		while len(point_stack) > 0:
			next_point = point_stack.pop()
			# Stopping case: reading a '#'
			if temp_tree[next_point] != '#':
				next_pt_is_term = temp_tree[next_point].IsTerminal()
				if (2*next_point+2) <= self.max_index and not next_pt_is_term:
					other_prog.tree[next_point] = temp_tree[next_point]
					point_stack.append(2*next_point + 1)
					point_stack.append(2*next_point + 2)
				elif next_pt_is_term:
					# Stopping case: terminal read
					other_prog.tree[next_point] = temp_tree[next_point]
				else:
					# Bad news: non-terminal read, but we're out of space in
					# the tree.  Pick a random terminal and stop this branch.
					other_prog.tree[next_point] = random.choice(self.nodeset.GetTerminals())
