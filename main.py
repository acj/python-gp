import evaluation
import representation
import program

tally = 0
count = 0
max_fit = 0
min_fit = 1
for x in range(1,10):
	prog = program.TreeProgram()
	prog.RaiseTree()

	# This is a known-working 3-mux tree:
	#prog2 = program.TreeProgram()
	#prog2.tree = ['O','A','A','1','N','2','0','-1','-1','0','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1', '-1']

	#print "Trees:"
	#print "\t" + prog.ToString()
	#print "\t" + prog2.ToString()

	#prog.Mutate(1, 0.25)
	#print "Mutated tree:"
	#print "\t" + prog.ToString()

	#prog.CrossOver(prog2)
	#print "CrossOver'd tree:"
	#print "\t" + prog.ToString()

	evaluator = evaluation.MultiplexerEvaluator()
	program_fitness = evaluator.Evaluate(prog)
	print "[Run %i]: %s" % (x, str(program_fitness))
	tally += program_fitness
	count += 1
	if program_fitness > max_fit:
		max_fit = program_fitness
	if program_fitness < min_fit:
		min_fit = program_fitness

print "[Avg] %f\t[Min] %f\t[Max] %f" % (float(tally)/count, min_fit, max_fit)
