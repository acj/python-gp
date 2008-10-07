import evaluation
import representation
import program

tally = 0
count = 0
for x in range(1,10):
	prog = program.TreeProgram()
	prog.RaiseTree()

	# This is a known-working 3-mux tree:
	#prog.tree = ['O','A','A','1','N','2','0','-1','-1','0']

	#print "Tree:"
	#print "\t" + prog.ToString()

	evaluator = evaluation.MultiplexerEvaluator()
	program_fitness = evaluator.Evaluate(prog)
	print "[Run %i]: %s" % (x, str(program_fitness))
	tally += program_fitness
	count += 1

print "[Avg] %f" % (float(tally)/count)
