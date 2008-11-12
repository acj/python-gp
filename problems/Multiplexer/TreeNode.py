class TreeNode:
	def __init__(self):
		self.terminal = True
		self.arity = 1
		self.value = None
		# Children
		self.left = None
		self.right = None

	def IsTerminal(self):
		return self.terminal

	def GetValue(self):
		return self.value

	def GetArity(self):
		return self.arity
