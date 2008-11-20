// Copyright Ralf W. Grosse-Kunstleve 2002-2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <cmath>
#include <iostream>
#include <string>

using namespace std;

class EvalTree
{
private:
	char *expression;
public:
	EvalTree()
	{
		expression = 0;
	}
	
	void set_expression(char *exp)
	{
		if (expression != 0)
		{
			free(expression);
		}
		expression = strdup(exp);
	}

	float evaluate_regression()
	{
		size_t num_of_pts = 100;
		float total_difference = 0.0;
		float curpt = -1.0;

		float dx_difference, expected;
		for (size_t ndx=0; ndx<num_of_pts; ++ndx) {
			expected = curpt*curpt+curpt+1;
			dx_difference = fabs(expected - evaluate_regression_expression(0, curpt));
			total_difference += dx_difference;
			curpt += 2.0/num_of_pts;
		}
		return total_difference;
	}

	float evaluate_regression_expression(size_t i, float curpt)
	{
		if (expression[i] != '+' && expression[i] != '-' && expression[i] != '*' && expression[i] != '/' && expression[i] != 'x')
		{
			return (float)atoi(&expression[i]);
		}
		float leftvalue = 0.0;
		float rightvalue = 0.0;

		size_t current = (2 * i) + 1;
		if (current < strlen(expression))
			leftvalue = evaluate_regression_expression(current, curpt);

		current = (2 * i) + 2;
		if (current < strlen(expression))
			rightvalue = evaluate_regression_expression(current, curpt);
		
		switch (expression[i])
		{
			case '+':
			{
				return leftvalue + rightvalue;
			}

			case '-':
			{
				return leftvalue - rightvalue;			
			}

			case '*':
			{
				return leftvalue * rightvalue;
			}
			
			case '/':
			{
				if (rightvalue == 0.0) {
					return 0.0;
				} else {
					return leftvalue / rightvalue;
				}
			}

			case 'x':
			{
				return curpt;
			}
			default:
			{
				cout << "Fell to default switch case" << endl;
				exit(1);
			}
		}
	}

	float evaluate_mux()
	{
		float total_correct = 0;
		char input[6];

		for (int s0=0; s0<=1; s0++)
		{
			input[0] = s0;
			for (int s1=0; s1<=1; s1++)
			{
				input[1] = s1;
				for (int a=0; a<=1; a++)
				{
					input[2] = a;
					for (int b=0; b<=1; b++)
					{
						input[3] = b;
						for (int c=0; c<=1; c++)
						{
							input[4] = c;
							for (int d=0; d<=1; d++)
							{
								input[5] = d;

								bool result = (a && !s0 && !s1) || 
									  (b && s0 && !s1) || 
									  (c && !s0 && s1) ||
									  (d && s0 && s1);
								if (evaluate_expression(0, input) == result)
								{
									total_correct += 1;
								}
							}
						}
					}
				}
			}
		}
		return (total_correct / 64);
	}

	//Using the inorder traversal method 
	bool evaluate_expression(int i, char *input)
	{
		if (expression[i] != 'A' && expression[i] != 'O' && expression[i] != 'N')
		{
			char operand = expression[i];
			int op = atoi(&operand);
			return input[op];
		}
		bool leftvalue = false;
		bool rightvalue = false;

		size_t current = (2 * i) + 1;
		if (current < strlen(expression))
			leftvalue = evaluate_expression(current, input);

		current = (2 * i) + 2;
		if (current < strlen(expression))
			rightvalue = evaluate_expression(current, input);
		
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
				cout << "Fell to default switch case" << endl;
				exit(1);
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
        .def("evaluate_mux", &EvalTree::evaluate_mux)
        .def("evaluate_regression", &EvalTree::evaluate_regression)
        //.def("evaluate_expression", &EvalTree::evaluate_expression)
        ;
}
