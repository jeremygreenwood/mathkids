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
# TODO include configuration to enable negative numbers
#      this should effect the random number generation for subraction to ensure the answer is non-negative
#      if enabled, random number generation should be between (-max, max) as opposed to the normal (0, max)


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

    @staticmethod
    def rand_get( maximum ):
        return randrange( 0, maximum )
    
    @staticmethod
    def math_func_add( a, b ):
        return a + b
        
    @staticmethod
    def math_func_subtract( a, b ):
        return a - b
        
    @staticmethod
    def math_func_multiply( a, b ):
        return a * b
        
    @staticmethod
    def math_func_divide( a, b ):
        # TODO avoid divide by zero
        return a / b

    def prob_add( self, problem ):
        self.problem_list.append( problem )
        
    def __init__( self ):
        self.problem_list = []
        
        # Set various operations
        add = MathType( BasicMath.math_func_add,      "+", MAX_INT_ADD      )
        sub = MathType( BasicMath.math_func_subtract, "-", MAX_INT_SUBTRACT )
        mul = MathType( BasicMath.math_func_multiply, "*", MAX_INT_MULTIPLY )
        div = MathType( BasicMath.math_func_divide,   "/", MAX_INT_DIVIDE   )
        
        self.prob_add( add )
        self.prob_add( sub )
        self.prob_add( mul )
        self.prob_add( div )
        
    
    def prob_gen( self, prob_type ):
        #""""Generate a math problem""""
        # Generate random numbers for math problem
        # TODO this may be best to associate with specific problem type (e.g. to avoid decimal numbers for division)
        self.num1 = BasicMath.rand_get( prob_type.max )
        self.num2 = BasicMath.rand_get( prob_type.max )
        
        # Compute the answer, avoiding divide by zeros    
        # TODO remove once addressed by using problem specific random integer values which will not have a denominator of zero
        try:
            self.answer = prob_type.func( self.num1, self.num2 )
        except ZeroDivisionError:
            # TODO remove
            self.answer = 0
            
        self.question_str = str( self.num1 ) + " " + problem.sym + " " + str( self.num2 ) + " = ?"
        self.answer_str   = str( self.num1 ) + " " + problem.sym + " " + str( self.num2 ) + " = " + str( self.answer )
            
        
    def prob_type_get( self ):
        """Returns a random math problem type that is enabled"""
        # TODO this should cross reference with enabled variable of each MathType (unless problem list is changed to only contain enabled problems)
        return random.choice( self.problem_list )
        
    def question_str_get( self ):
        return self.question_str
        
    def answer_int_get( self ):
        return self.answer
        
    def answer_str_get( self ):
        return self.answer_str
        
        

#class MathKids(BasicMath):
#    """Main class for mathkids game"""
    

#-------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------
    
    
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
# TODO create a __main__ function

# Create a list of math problem types, such that a random problem type may be used
# TODO consider adding "enabled" as a configuration setting and only adding enabled problem types to the list
basic_math = BasicMath()


# Continually ask arithmetic problems
while True:
    
    # Set current math operation randomly
    problem = basic_math.prob_type_get()
    
    # Generate a math problem for the type of problem which was chosen randomly in the previous statement
    basic_math.prob_gen( problem )
    
    # Print the math problem as a question
    print basic_math.question_str_get()
    
    # Get answer from user
    user_answer = user_input_get()
    
    # Print whether they got the math problem correct, and supply the answer if incorrect
    if user_answer == basic_math.answer_int_get():
        print "Correct, good job!"
    else:
        print "That's not right, good try. Here's the answer:"
        print basic_math.answer_str_get()
    
    print "---------------------------------------------------"
    