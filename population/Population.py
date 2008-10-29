import random

class Population:
	"""A standard GP population"""

	def __init__(self, pop_size, program_class, evaluator_class):
		self.pop = []
		self.fitness_grid = []
		self.average_fitness = 0.0
		self.best_fitness = (-1, 0)
		self.program_class = program_class # Save for making children
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
			if len(prog.tree) == 0:
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

		# Selection...
		prog1 = None
		prog2 = None
		# Select a random organism weighted by fitness (better fitness
		# increases probability of selection)
		fit_total = sum(self.fitness_grid)
		n = random.uniform(0, fit_total)
		for ndx in range(1, len(self.pop) - 1):
			if n < self.fitness_grid[ndx]:
				prog1 = self.pop[ndx]
				break
			n = n - self.fitness_grid[ndx]
		if prog1 == None:
			prog1 = self.pop[0]

		# Same selection process again
		n = random.uniform(0, fit_total)
		for ndx in range(1, len(self.pop) - 1):
			if n < self.fitness_grid[ndx]:
				prog2 = self.pop[ndx]
				break
			n = n - self.fitness_grid[ndx]
		if prog2 == None:
			prog2 = self.pop[len(self.pop)-1]

		# Mutation...
		if random.random() < 0.1:
			rand_org = random.choice(self.pop)
			rand_org.Mutate(1, 1.0)
		
		# Crossover...
		prog_child = self.program_class()
		prog_child.tree = list(prog1.tree) # Shallow list copy
		prog_child.CrossOver(prog2, 0.2)

		# If crossover had an effect, let's insert the child
		if prog_child.tree != prog1.tree:
			#new_child_index = random.randint(1, len(self.pop) - 1)
			#self.pop[new_child_index] = prog_child
			new_child_index = sorted_grid[1]
			self.pop[new_child_index] = prog_child

			child_fit = self.evaluator.Evaluate(prog_child)
			self.fitness_grid[new_child_index] = child_fit

			# If this program was the best before it got crossed over, then
			# we need to give the crown to the second-best program
			# TODO: Fix this to work again
			#if self.best_fitness[0] == sorted_grid[-1]:
			#	self.best_fitness = (sorted_grid[-2], self.fitness_grid[sorted_grid[-2]])

			# Re-evaluate the new (crossed-over) fitness against the best fitness
			self.fitness_grid[sorted_grid[-1]] = child_fit
			if child_fit > self.best_fitness[1]:
				self.best_fitness = (sorted_grid[-1], child_fit)

		# TODO: Export this data in CSV (or similar) format
		#(prog1_fit, prog2_fit) = (self.fitness_grid[sorted_grid[1]], self.fitness_grid[sorted_grid[-2]])
		#print "XO: %f + %f = %f (Delta: %f)" % (prog1_fit, prog2_fit, child_fit, child_fit - max(prog1_fit, prog2_fit))

		#print "Best of run: (%i, %f)" %  self.best_fitness
		#print "Average: %f" % self.average_fitness
