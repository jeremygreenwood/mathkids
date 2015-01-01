#!/usr/bin/python
# TODO create library functions to make the high level parts of the program very easy for kids to read
# TODO add usage statement
# TODO add colorizing: green when correct, red when incorrect
# TODO add parameters to only ask questions for add, sub, mult, div, random, or cycle through
#      perhaps have option to configure for automatic selection based on the day of the week
# TODO add profiles to keep track of session logs and difficulty settings
#      may want to forgo profiles in favor of multiple installations
# TODO add logging of each session (and print a summary of results) to time-stamped file in a directory based on user profile
# TODO add learning functionality:
#      if a question has been answered correctly many times it should be omitted
#      if too many questions are omitted then the maximum range value for the type of problem should be increased


import random
from random import randrange


# Set configurations
# TODO read configs from a settings file, and use a default if the settings file DNE
MAX_INT_ADD      = 16
MAX_INT_SUBTRACT = 8
MAX_INT_MULTIPLY = 4
MAX_INT_DIVIDE   = 2


#-------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------
class MathType:
    """Math problem type class, defines a type of math problem and its characteristics."""
    def __init__( self, function, symbol, maximum ):
        self.func = function
        self.sym = symbol
        self.max = maximum
        self.enabled = False
        

# TODO can/should this be a subclass of MathType
class BasicMath:
    """Basic mathematics class, manages list of different types of math problems."""  
    
    problem_list = []
    
    def math_func_add( a, b ):
        return a + b
        
    def math_func_subtract( a, b ):
        return a - b
        
    def math_func_multiply( a, b ):
        return a * b
        
    def math_func_divide( a, b ):
        # TODO avoid divide by zero
        return a / b

    def prob_add( problem ):
        BasicMath.problem_list.append( problem )
        
    math_func_add = staticmethod( math_func_add )        
    math_func_subtract = staticmethod( math_func_subtract )        
    math_func_multiply = staticmethod( math_func_multiply )        
    math_func_divide = staticmethod( math_func_divide )
    prob_add = staticmethod( prob_add )
        
    def __init__( self ):
#        self.problem_list = []
        
        # Set various operations
        add = MathType( BasicMath.math_func_add,      "+", MAX_INT_ADD      )
        sub = MathType( BasicMath.math_func_subtract, "-", MAX_INT_SUBTRACT )
        mul = MathType( BasicMath.math_func_multiply, "*", MAX_INT_MULTIPLY )
        div = MathType( BasicMath.math_func_divide,   "/", MAX_INT_DIVIDE   )
        
        BasicMath.prob_add( add )
        BasicMath.prob_add( sub )
        BasicMath.prob_add( mul )
        BasicMath.prob_add( div )
        
    
#    def gen_prob( self )
#        """"Generate a math problem""""
    
    def prob_type_get( self ):
        """Returns a random math problem type that is enabled"""
        # TODO this should cross reference with enabled variable of each MathType
        return random.choice( BasicMath.problem_list )
        
        

#class MathKids(BasicMath):
#    """Main class for mathkids game"""
    

#-------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------
def rand_get( maximum ):
    return randrange( 0, maximum )
    
    
def user_input_get():
    while True:
        try:
            user_input = int( raw_input( "Enter answer: " ) )
            return user_input
        except ValueError:
            print "Answer not recognized."
            pass
    
    
#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------


# Create a list of math problem types, such that a random problem type may be used
# TODO consider adding "enabled" as a configuration setting and only adding enabled problem types to the list
#prob_types = [ add, sub, mul, div ]
basic_math = BasicMath()


# Continually ask arithmetic problems
while True:
    
    # Set current math operation randomly
    math = basic_math.prob_type_get()
    
    # Generate random numbers for math problem
    # TODO this may be best to associate with specific problem type (e.g. to avoid decimal numbers for division)
    num1 = rand_get( math.max )
    num2 = rand_get( math.max )
    
    # Compute the answer, avoiding divide by zeros    
    # TODO remove once addressed by using problem specific random integer values which will not have a denominator of zero
    try:
        real_answer = math.func( num1, num2 )
    except ZeroDivisionError:
        continue
    
    # Print the math problem as a question
    print num1,math.sym,num2,"= ?"
    
    # Get answer from user
    user_answer = user_input_get()
    
    # Print whether they got the math problem correct, and supply the answer if incorrect
    if user_answer == real_answer:
        print "Correct, good job!"
    else:
        print "That's not right, good try. Here's the answer:"
        print num1,math.sym,num2,"=",real_answer
    
    print "---------------------------------------------------"
    