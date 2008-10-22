// Copyright Ralf W. Grosse-Kunstleve 2002-2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <iostream>
#include <string>

class EvalTree
{
private:
	char *expression;
public:
	EvalTree()
	{
	}
	
	void set_expression(char *exp)
	{
		expression = strdup(exp);
	}

	//Using the inorder traversal method 
	bool evaluate_expression(int i)
	{
		if (expression[i] != 'A' && expression[i] != 'O' && expression[i] != 'N')
		{
			char operand = expression[i];
			int op = atoi(&operand);
			return op;

		}
		bool leftvalue = false;
		bool rightvalue = false;

		size_t current = (2 * i) + 1;
		if (current < strlen(expression))
			leftvalue = evaluate_expression(current);

		current = (2 * i) + 2;
		if (current < strlen(expression))
			rightvalue = evaluate_expression(current);
		
		switch (expression[i])
		{
			case 'A':
			{
				return leftvalue && rightvalue;
			}

			case 'O':
			{
				return leftvalue || rightvalue;			
			}

			case 'N':
			{
				if (expression[2*i+1] == '#') 
					return !rightvalue;
				else
					return !leftvalue;		
			}
			default:
			{
				std::cerr << "Fell to default case; should never happen!" << std::endl;
				exit(EXIT_FAILURE);
			}
		}
	}
};

BOOST_PYTHON_MODULE(hybridgp)
{
    using namespace boost::python;
    class_<EvalTree>("EvalTree")
        // Add a regular member function.
		.def("set_expression", &EvalTree::set_expression)
        .def("evaluate_expression", &EvalTree::evaluate_expression)
        ;
}
