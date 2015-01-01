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
        

# TODO can/should this be a subclass of MathType
class BasicMath:
    """Basic mathematics class, manages list of different types of math problems."""
    def __init__( self ):
        self.type = []

    def add( self, problem ):
        self.type.append( problem )


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


# TODO should probably move within basic math class
def math_func_add( a, b ):
    return a + b


def math_func_subtract( a, b ):
    return a - b


def math_func_multiply( a, b ):
    return a * b


def math_func_divide( a, b ):
    # TODO avoid divide by zero
    return a / b
    
    
#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
# Set various operations
# TODO can this functionality be pushed into the BasicMath class
add = MathType( math_func_add,      "+", MAX_INT_ADD      )
sub = MathType( math_func_subtract, "-", MAX_INT_SUBTRACT )
mul = MathType( math_func_multiply, "*", MAX_INT_MULTIPLY )
div = MathType( math_func_divide,   "/", MAX_INT_DIVIDE   )

# Create a list of math problem types, such that a random problem type may be used
# TODO consider adding "enabled" as a configuration setting and only adding enabled problem types to the list
#prob_types = [ add, sub, mul, div ]
math_prob = BasicMath()
math_prob.add( add )
math_prob.add( sub )
math_prob.add( mul )
math_prob.add( div )


# Continually ask arithmetic problems
while True:
    
    # Set current math operation randomly
    math = random.choice( math_prob.type )
    
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