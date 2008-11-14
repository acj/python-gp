import random

def NormInverse(lst):
	max_fit = max(lst)
	inv_lst = []
	# Invert and normalize the list
	for x in lst:
		inv_lst.append(1.0-(x/max_fit))
	return inv_lst

def RandomSelect(problem, fitness_lst):
	return random.randint(0, len(fitness_lst)-1)

def RouletteWheelSelect(problem, fitness_lst):
	chosen_ndx = None
	fitnesses = None
	if problem.IsMaximizationProblem():
		fitnesses = fitness_lst
	else:
		fitnesses = NormInverse(fitness_lst)
	fit_total = sum(fitnesses)
	n = random.uniform(0, fit_total)
	for ndx in range(1, len(fitnesses)):
		if n < fitnesses[ndx]:
			chosen_ndx = ndx
			break
		n = n - fitnesses[ndx]
	# Provide a fail-safe for when the algorithm fails to select
	# an individual
	if chosen_ndx == None:
		chosen_ndx = random.randint(0, len(fitnesses)-1)
	return chosen_ndx

def TournamentSelect(problem, fitness_lst, tournament_size=10):
	"""Selects an individual according to tournament selection.  Returns 
	the index in the fitness list corresponding to the selected 
	individual."""
	tournament_best = None
	tournament_best = None
	for n in range(0, tournament_size):
		ndx = random.randint(0, len(fitness_lst) - 1)
		prog_fit = fitness_lst[ndx]
		if tournament_best == None:
			tournament_best = n
		else:
			if problem.IsMaximizationProblem() and prog_fit > tournament_best:
				tournament_best = n
			elif prog_fit < tournament_best:
				# Minimization problem
				tournament_best = n
	return n
