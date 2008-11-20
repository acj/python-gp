import evaluation
import gp
import representation
import problems
import population

#ev = problems.Regression.RegressionEvaluator()
ev = problems.Regression.CPPRegressionEvaluator()
problem = problems.Regression.RegressionProblem(ev)
pop = population.Population(100, problem, 0.90, 0.05, 0.10, gp.RouletteWheelSelect, gp.RouletteWheelSelect, gp.RouletteWheelSelect)

# Set up counters
update_count = 0
best_of_run = (0, 10000000.0, '')

try:
	while pop.best_fitness[1] > 0.0:
		pop.DoStep()
		update_count += 1
		if pop.best_fitness[1] < best_of_run[1]:
			best_of_run = (pop.best_fitness[0], pop.best_fitness[1], pop.pop[pop.best_fitness[0]].Pickle())
		if update_count % 1 == 0:
			if pop.best_fitness[1] < 0.000001:
				print "Best of generation #%i: (%i, %.6e); avg fitness = %f" % (update_count, pop.best_fitness[0], pop.best_fitness[1], pop.average_fitness)
			else:
				print "Best of generation #%i: (%i, %f); avg fitness = %f" % (update_count, pop.best_fitness[0], pop.best_fitness[1], pop.average_fitness)
	
	# If we reach an ideal individual, simulate an interrupt
	raise KeyboardInterrupt
except KeyboardInterrupt:
	print "---"
	print "Best of run: %d, %f, %s" % best_of_run
