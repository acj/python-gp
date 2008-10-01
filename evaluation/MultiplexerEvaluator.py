import Evaluator
import math

class MultiplexerEvaluator(Evaluator.Evaluator):
	"""Multiplexer evaluator"""

	def __init__(self, dataLines):
		self.dataLines = dataLines
		self.ctrlLines = int(math.ceil(math.log(self.dataLines, 2)))
		if round(self.ctrlLines) != self.ctrlLines:
			print >>sys.stderr, "The number of data lines must be an integer"
		self.totalLines = self.dataLines + self.ctrlLines

	def evaluate(self, input):
		if len(input) != self.totalLines:
			raise ValueError

		factor = 1
		line = 0
		startingIndex = self.ctrlLines - 1

		for i in range(startingIndex, -1, -1):
			if input[i] == 1:
				line += factor;

			factor <<= 1

			return input[self.ctrlLines + line]
