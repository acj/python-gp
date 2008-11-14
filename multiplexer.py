import evaluation
import representation
import problems
import population

ev = problems.Multiplexer.MultiplexerEvaluator()
problem = problems.Multiplexer.MultiplexerProblem(ev)
pop = population.Population(100, problem, 0.60, 0.10, 0.30)

# Set up counters
update_count = 0
best_of_run = (0, 0.0, '')

try:
	while pop.best_fitness[1] < 1.0:
		pop.DoStep()
		update_count += 1
		if pop.best_fitness[1] > best_of_run[1]:
			best_of_run = (pop.best_fitness[0], pop.best_fitness[1], pop.pop[pop.best_fitness[0]].Pickle())
		if update_count % 10 == 0:
			print "Best of generation #%i: (%i, %f); avg fitness = %f" % (update_count, pop.best_fitness[0], pop.best_fitness[1], pop.average_fitness)
except KeyboardInterrupt:
	print "---"
	print "Best of run: %d, %f, %s" % best_of_run
