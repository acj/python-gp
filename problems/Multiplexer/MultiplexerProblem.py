import MultiplexerNodes
import representation

class MultiplexerProblem:
	def __init__(self, eval_instance):
		self.ev = eval_instance
		self.ideal_fitness = 1.0
		self.nodeset = MultiplexerNodes.MultiplexerNodes()
		self.tree_depth = 8 
	
	def GetEvaluator(self):
		return self.ev

	def GetNodeSet(self):
		return self.nodeset
	
	def GetNewProgramInstance(self):
		return representation.Tree(self.tree_depth, self.nodeset)
	
	def IsMaximizationProblem(self):
		return True
