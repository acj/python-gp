class Population:
	"""A standard GP population"""

	def __init__(self, pop_size, program_class, evaluator_class):
		self.pop = []
		self.fitness_grid = []
		self.average_fitness = 0.0
		self.best_fitness = (-1, 0)
		idx = 0
		while idx < pop_size:
			self.pop.append(program_class())
			self.fitness_grid.append(0.0)
			idx += 1

		# Get an evaluator instance to use
		self.evaluator = evaluator_class()

	def DoStep(self):
		"""Perform an evolutionary step.  `Execute' each program,
		perform mutation/crossover and selection, and then stop."""
		self.best_fitness = (0,0) # (organism index, organism fitness)

		# Evaluation...
		total_fitness = 0.0
		for ndx in range(0, len(self.pop)):
			prog = self.pop[ndx]
			if prog.tree == []:
				prog.RaiseTree()
			self.fitness_grid[ndx] = self.evaluator.Evaluate(prog)
			if self.fitness_grid[ndx] > self.best_fitness[1]:
				self.best_fitness = (ndx, self.fitness_grid[ndx])
			total_fitness += self.fitness_grid[ndx]

		self.average_fitness = total_fitness / len(self.pop)
		
		#print "Fitnesses:"
		#for fitness in self.fitness_grid:
		#	print "\t%f" % fitness

		# This constructs a sorted List (INDICES ONLY) of fitnesses in
		# ascending order.
		sorted_grid = list(index for index, item in sorted(enumerate(self.fitness_grid), key=lambda item: item[1]))

		# Mutation...
		for ndx in range(0, len(self.pop)):
			self.pop[ndx].Mutate(1, 0.10)

		# Selection...
		# TODO: Try to use something better (e.g., fitness proportional)
		prog1 = self.pop[sorted_grid[-1]]
		prog2 = self.pop[sorted_grid[-2]]
		
		# Crossover...

		# TODO: Use a copy of prog1 and overwrite an old organism with
		# the child
		prog1.CrossOver(prog2)

		(prog1_fit, prog2_fit) = (self.fitness_grid[sorted_grid[1]], self.fitness_grid[sorted_grid[-2]])
		child_fit = self.evaluator.Evaluate(prog1)

		# If this program was the best before it got crossed over, then
		# we need to give the crown to the second-best program
		if self.best_fitness[0] == sorted_grid[-1]:
			self.best_fitness = (sorted_grid[-2], self.fitness_grid[sorted_grid[-2]])

		# Re-evaluate the new (crossed-over) fitness against the best fitness
		self.fitness_grid[sorted_grid[-1]] = child_fit
		if child_fit > self.best_fitness[1]:
			self.best_fitness = (sorted_grid[-1], child_fit)

		# TODO: Export this data in CSV (or similar) format
		#print "XO: %f + %f = %f (Delta: %f)" % (prog1_fit, prog2_fit, child_fit, child_fit - max(prog1_fit, prog2_fit))

		print "Best of run: (%i, %f)" %  self.best_fitness
		print "Average: %f" % self.average_fitness
