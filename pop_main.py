import evaluation
import representation
import program
import population

tally = 0
count = 0
max_fit = 0
min_fit = 1
#for x in range(1,10):
update_count = 0
#pop = population.Population(50, program.TreeProgram, evaluation.MultiplexerEvaluator)
pop = population.Population(50, program.TreeProgram, evaluation.CPPMuxEvaluator)
while True: #pop.best_fitness[1] < 1.0:
	pop.DoStep()
	update_count += 1
	if (update_count % 250) == 0:
		print "== %i ==" % update_count
		print "Best of run: (%i, %f)" %  pop.best_fitness
		print "Average: %f" % pop.average_fitness
	if pop.best_fitness[1] == 1.0:
		print "Resulting tree (index %i) after %i generations:" % (pop.best_fitness[0], update_count)
		print "\t%s" % pop.pop[pop.best_fitness[0]].ToString()
		print "\t%s" % pop.pop[pop.best_fitness[0]].Pickle()
		sys.exit(0)
