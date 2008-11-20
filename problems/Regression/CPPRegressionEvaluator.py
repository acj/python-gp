import evaluation
import hybridgp
import math

class CPPRegressionEvaluator(evaluation.Evaluator):
	"""Regression evaluator"""

	def __init__(self):
		self.evaltree = hybridgp.EvalTree()
		pass

	def Evaluate(self, program):
		#print "Pickled: %s" % ''.join(program.BriefPickle())
		self.evaltree.set_expression(program.BriefPickle())
		return self.evaltree.evaluate_regression()
