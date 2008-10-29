import Evaluator
import hybridgp

class CPPMuxEvaluator(Evaluator.Evaluator):
	
	def __init__(self):
		self.evaltree = hybridgp.EvalTree()
	
	def Evaluate(self, program):
		self.evaltree.set_expression(''.join(program.tree))
		return self.evaltree.evaluate()
