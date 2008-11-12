import evaluation
import representation
import problems
import program
import population

ev = problems.Multiplexer.MultiplexerEvaluator()
problem = problems.Multiplexer.MultiplexerProblem(ev)
pop = population.Population(100, problem)

# Set up counters
tally = 0
count = 0
max_fit = 0
min_fit = 1
update_count = 0
while pop.best_fitness[1] < 1.0:
	pop.DoStep()
	update_count += 1
	if (update_count % 50) == 0:
		print "== %i ==" % update_count
		print "Best of run #%i: (%i, %f)" %  (update_count, pop.best_fitness[0], pop.best_fitness[1])
		print "Average: %f" % pop.average_fitness
	if pop.best_fitness[1] == 1.0:
		print "Resulting tree (index %i) after %i generations:" % (pop.best_fitness[0], update_count)
		print "\t%s" % pop.pop[pop.best_fitness[0]].ToString()
		print "\t%s" % pop.pop[pop.best_fitness[0]].Pickle()
