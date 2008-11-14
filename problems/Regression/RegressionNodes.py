import representation

class PlusNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "PlusNode()"
		self.terminal = False
		self.arity = 2
		self.value = "+"

class MinusNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "MinusNode()"
		self.terminal = False
		self.arity = 2
		self.value = "-"

class MultiplyNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "MultiplyNode()"
		self.terminal = False
		self.arity = 2
		self.value = "*"

class DivideNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "DivideNode()"
		self.terminal = False
		self.arity = 2
		self.value = "/"

class VariableNode(representation.TreeNode):
	def __init__(self):
		# General properties
		self.name = "VariableNode()"
		self.terminal = True
		self.arity = 0
		self.value = "x"

class IntegerNode(representation.TreeNode):
	def __init__(self, value):
		# General properties
		self.name = "IntegerNode(" + str(value) + ")"
		self.terminal = True
		self.arity = 0
		self.value = str(value)

class RegressionNodes(representation.TreeNodeSet):
	def __init__(self):
		self.nodes = [PlusNode(), MinusNode(), MultiplyNode(), VariableNode(), 
		#DivideNode(), 
		#IntegerNode(-5.0),
		#IntegerNode(-4.0), IntegerNode(-3.0), IntegerNode(-2.0),
		IntegerNode(-1.0), IntegerNode(0.0), IntegerNode(1.0),
		#IntegerNode(2.0), IntegerNode(3.0), IntegerNode(4.0),
		#IntegerNode(5.0) ]
		]

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
