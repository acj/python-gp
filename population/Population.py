import random

class Population:
	"""A standard GP population"""

	def __init__(self, pop_size, problem_instance, xo_prob, repro_prob, mut_prob):
		self.pop = []
		self.fitness_grid = []
		self.average_fitness = 0.0
		self.best_fitness = (-1, 0.50)
		self.problem = problem_instance
		# Probabilities
		self.xo_prob = xo_prob
		self.repro_prob = repro_prob
		self.mut_prob = mut_prob
		idx = 0
		while idx < pop_size:
			self.pop.append(self.problem.GetNewProgramInstance())
			self.fitness_grid.append(0.0)
			# Use a mix of full and non-full trees
			if random.random() <= 0.85:
				self.pop[idx].RaiseTree(True)
			else:
				self.pop[idx].RaiseTree(False)
			idx += 1

		# Get an evaluator instance to use
		self.evaluator = self.problem.GetEvaluator()

	def NormInverse(self, lst):
		max_fit = max(lst)
		inv_lst = []
		# Invert and normalize the list
		for x in lst:
			inv_lst.append(1.0-(x/max_fit))
		return inv_lst

	def DoStep(self):
		"""Perform an evolutionary step.  `Execute' each program,
		perform selection and mutation/crossover, and then stop."""
		if self.problem.IsMaximizationProblem():
			self.best_fitness = (0,0.0) # (organism index, organism fitness)
		else:
			self.best_fitness = (0,1000000.0) # (organism index, organism fitness)
		# Evaluation...
		total_fitness = 0.0
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
				
			total_fitness += self.fitness_grid[ndx]

		self.average_fitness = total_fitness / len(self.pop)

		# If we've found an ideal individual, then stop
		if self.best_fitness[1] == self.problem.ideal_fitness:
			print "*** Ideal individual found ***"
			print self.pop[self.best_fitness[0]].ToString()
			print self.pop[self.best_fitness[0]].Pickle()

		
		# This constructs a sorted List (INDICES ONLY) of fitnesses in
		# ascending order.
		sorted_grid = list(index for index, item in sorted(enumerate(self.fitness_grid), key=lambda item: item[1]))

		#for x in sorted_grid:
		#	print self.fitness_grid[x]

		# Select a random organism weighted by fitness (better fitness
		# increases probability of selection)
		new_pop = []

		#print "Min, max = (%f, %f)" % (min_fit, max_fit)
		#tournament_size = 25 
		#tournament_best = None
		#while len(new_pop) < 0.90*len(self.pop):
		#	tournament_best = None
		#	tourn_prog = self.problem.GetNewProgramInstance()
		#	for n in range(0, tournament_size):
		#		ndx = random.randint(0, len(self.pop) - 1)
		#		prog_fit = self.fitness_grid[ndx]
		#		if tournament_best == None:
		#			tournament_best = (n, prog_fit)
		#		else:
		#			if self.problem.IsMaximizationProblem() and prog_fit > tournament_best[1]:
		#				tournament_best = (n, prog_fit)
		#			elif prog_fit < tournament_best[1]:
		#				# Minimization problem
		#				tournament_best = (n, prog_fit)
		#	tourn_prog.tree = list(self.pop[tournament_best[0]].tree)
		#	new_pop.append(tourn_prog)
		#	print "Adding program #%d with fitness %f" % (tournament_best[0], tournament_best[1])

		#TODO: Split the different selection techniques into functions
		fit_total = 0
		if self.problem.IsMaximizationProblem():
			fit_total = sum(self.fitness_grid)
		else:
			self.fitness_grid = self.NormInverse(self.fitness_grid)
			fit_total = sum(self.fitness_grid)

		while len(new_pop) < 0.50*len(self.pop):
			n = random.uniform(0, fit_total)
			for ndx in range(1, len(self.pop)):
				if n < self.fitness_grid[ndx]:
					new_pop.append(self.pop[ndx])
					break
				n = n - self.fitness_grid[ndx]

		while len(new_pop) < len(self.pop):
			prog1 = self.problem.GetNewProgramInstance()
			prog2 = self.problem.GetNewProgramInstance()
			prog1.tree = list(new_pop[random.randint(0,len(new_pop)-1)].tree)
			prog2.tree = list(new_pop[random.randint(0,len(new_pop)-1)].tree)

			if random.random() < self.xo_prob:
				prog1.CrossOver(prog2)
				new_pop.append(prog1)
				# Use both modified programs if we have space available
				if len(new_pop) < len(self.pop):
					new_pop.append(prog2)
			elif random.random() < self.repro_prob:
				# Reproduction -- copy the parent(s) as-is
				new_pop.append(prog1)
				if len(new_pop) < len(self.pop):
					new_pop.append(prog2)
			
		self.pop = new_pop

		# Mutation...
		for mut_org in self.pop:
			mut_org.Mutate(1, self.mut_prob)
