import gp
import operator
import random

class Population:
	"""A standard GP population"""

	def __init__(self, pop_size, problem, xo_prob, repro_prob, mut_prob, xo_select, repro_select, mut_select):
		self.pop = []
		self.fitness_grid = []
		self.average_fitness = 0.0
		self.best_fitness = (-1, 0.50)
		self.problem = problem
		# Probabilities
		self.xo_prob = xo_prob
		self.repro_prob = repro_prob
		self.mut_prob = mut_prob
		# Selection algorithms
		self.xo_select = xo_select
		self.repro_select = repro_select
		self.mut_select = mut_select
		# Create initial population
		for idx in range(0, pop_size):
			self.pop.append(self.problem.GetNewProgramInstance())
			self.fitness_grid.append(0.0)
			# Use a mix of full and non-full trees
			if random.random() <= 0.85:
				self.pop[idx].RaiseTree(True)
			else:
				self.pop[idx].RaiseTree(False)
		# Get an evaluator instance to use
		self.evaluator = self.problem.GetEvaluator()

	def DoEvaluation(self):
		for ndx in range(0, len(self.pop)):
			self.fitness_grid[ndx] = self.evaluator.Evaluate(self.pop[ndx])
			if self.problem.IsMaximizationProblem():
				# Maximization 
				if self.fitness_grid[ndx] > self.best_fitness[1]:
					self.best_fitness = (ndx, self.fitness_grid[ndx])
			else:
				# Minimization
				if self.fitness_grid[ndx] < self.best_fitness[1]:
					self.best_fitness = (ndx, self.fitness_grid[ndx])
				
		self.average_fitness = reduce(operator.add,self.fitness_grid) / len(self.fitness_grid)

	def DoStep(self):
		"""Perform an evolutionary step.  `Execute' each program,
		perform selection and mutation/crossover, and then stop."""
		if self.problem.IsMaximizationProblem():
			self.best_fitness = (0,0.0) # (organism index, organism fitness)
		else:
			self.best_fitness = (0,1000000.0) # (organism index, organism fitness)
		self.DoEvaluation()

		# If we've found an ideal individual, then stop
		if self.best_fitness[1] == self.problem.ideal_fitness:
			print "*** Ideal individual found ***"
			print self.pop[self.best_fitness[0]].ToString()
			print self.pop[self.best_fitness[0]].Pickle()
		
		# This constructs a sorted List (INDICES ONLY) of fitnesses in
		# ascending order.
		sorted_grid = list(index for index, item in sorted(enumerate(self.fitness_grid), key=lambda item: item[1]))

		# Grow a new generation
		new_pop = []

		while len(new_pop) < len(self.pop):
			if random.random() < self.xo_prob:
				prog1 = self.problem.GetNewProgramInstance()
				prog2 = self.problem.GetNewProgramInstance()
				ndx1 = self.xo_select(self.problem, self.fitness_grid)
				ndx2 = self.xo_select(self.problem, self.fitness_grid)
				prog1.tree = list(self.pop[ndx1].tree)
				prog2.tree = list(self.pop[ndx2].tree)
				prog1.CrossOver(prog2)
				new_pop.append(prog1)
				# Use both modified programs if we have space available
				if len(new_pop) < len(self.pop):
					new_pop.append(prog2)
			elif random.random() < self.repro_prob:
				# Reproduction -- copy the parent(s) as-is
				prog1 = self.problem.GetNewProgramInstance()
				ndx = self.repro_select(self.problem, self.fitness_grid)
				prog1.tree = list(self.pop[ndx].tree)
				new_pop.append(prog1)
			elif random.random() < self.mut_prob:
				prog_mut = self.problem.GetNewProgramInstance()
				ndx = self.mut_select(self.problem, self.fitness_grid)
				prog_mut.tree = list(self.pop[ndx].tree)
				prog_mut.Mutate()
				new_pop.append(prog_mut)
			
		self.pop = new_pop
