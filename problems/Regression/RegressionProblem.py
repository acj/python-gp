import RegressionNodes
import representation

class RegressionProblem:
	def __init__(self, eval_instance):
		self.ev = eval_instance
		self.ideal_fitness = 0.0
		self.nodeset = RegressionNodes.RegressionNodes()
		self.tree_depth = 4
	
	def GetEvaluator(self):
		return self.ev

	def GetNodeSet(self):
		return self.nodeset
	
	def GetNewProgramInstance(self):
		return representation.Tree(self.tree_depth, self.nodeset)

	def IsMaximizationProblem(self):
		return False
