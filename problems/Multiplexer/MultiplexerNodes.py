import representation

class AndNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "AND"
		self.terminal = False
		self.arity = 2
		self.value = "A"

class OrNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "OR"
		self.terminal = False
		self.arity = 2
		self.value = "O"

class NotNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "NOT"
		self.terminal = False
		self.arity = 1 
		self.value = "N"

class IntegerNode(representation.TreeNode):
	def __init__(self, value):
		# General properties
		self.name = "Int(" + str(value) + ")"
		self.terminal = True
		self.arity = 0
		self.value = str(value)

class MultiplexerNodes(representation.TreeNodeSet):
	def __init__(self):
		self.nodes = [AndNode(), OrNode(), NotNode(), IntegerNode(0),
		IntegerNode(1), IntegerNode(2), IntegerNode(3),
		IntegerNode(4), IntegerNode(5), ]

	def GetNonterminals(self):
		#return [x for x in self.nodes if not x.IsTerminal()]
		nonterm = []
		for n in self.nodes:
			if not n.IsTerminal():
				nonterm.append(n)
		return nonterm

	def GetTerminals(self):
		#return [x for x in self.nodes if x.IsTerminal()]
		term = []
		for n in self.nodes:
			if n.IsTerminal():
				term.append(n)
		return term
	
	def GetNodesByArity(self, arity):
		return [x for x in self.nodes if x.GetArity() == arity]
