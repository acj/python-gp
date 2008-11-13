import random

class Population:
	"""A standard GP population"""

	def __init__(self, pop_size, problem_instance):
		self.pop = []
		self.fitness_grid = []
		self.average_fitness = 0.0
		self.best_fitness = (-1, 0.01)
		self.problem = problem_instance
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
		
		# This constructs a sorted List (INDICES ONLY) of fitnesses in
		# ascending order.
		sorted_grid = list(index for index, item in sorted(enumerate(self.fitness_grid), key=lambda item: item[1]))

		#for x in sorted_grid:
		#	print self.fitness_grid[x]

		# Selection
		xover_prob 	= 0.10 	# Crossover probability
		reprod_prob	= 0.10	# Reproduction (parent copy) probability
		mutate_prob = 0.01	# Mutation probability

		# Select a random organism weighted by fitness (better fitness
		# increases probability of selection)
		new_pop = []

		tourn_prog = self.problem.GetNewProgramInstance()
		tournament_size = 10
		tournament_best = None
		while len(new_pop) < 0.5*len(self.pop):
			for n in range(0, tournament_size):
				ndx = random.randint(0, len(self.pop) - 1)
				prog_fit = self.fitness_grid[ndx]
				if tournament_best == None:
					tournament_best = (n, prog_fit)
				else:
					if self.problem.IsMaximizationProblem() and prog_fit > tournament_best[1]:
						tournament_best = (n, prog_fit)
					elif prog_fit < tournament_best[1]:
						# Minimization problem
						tournament_best = (n, prog_fit)

			new_pop.append(self.pop[tournament_best[0]])

		prog1 = None
		prog2 = None
		while len(new_pop) < len(self.pop):
			prog1 = new_pop[random.randint(0,len(new_pop)-1)]
			prog2 = new_pop[random.randint(0,len(new_pop)-1)]

			if prog1.tree != [] and prog2.tree != [] and random.random() < xover_prob:
				prog1.CrossOver(prog2)
				new_pop.append(prog1)
				# Use both modified programs if we have space available
				if len(new_pop) < len(self.pop):
					new_pop.append(prog2)
			elif random.random() < reprod_prob:
				# Reproduction -- copy the parent(s) as-is
				new_pop.append(prog1)
				if len(new_pop) < len(self.pop):
					new_pop.append(prog2)
			
		self.pop = new_pop

		# Mutation...
		for mut_org in self.pop:
			mut_org.Mutate(1, mutate_prob)
