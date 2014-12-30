#!/usr/bin/python
# TODO create library functions to make the high level parts of the program very easy for kids to read
# TODO add usage statement
# TODO add colorizing: green when correct, red when incorrect
# TODO add parameters to only ask questions for add, sub, mult, div, random, or cycle through
#      perhaps have option to configure for automatic selection based on the day of the week
# TODO add profiles to keep track of session logs and difficulty settings
# TODO add logging of each session (and print a summary of results) to time-stamped file in a directory based on user profile
# TODO add learning functionality:
#      if a question has been answered correctly many times it should be omitted
#      if too many questions are omitted then the maximum range value for the type of problem should be increased


from random import randrange

MAX_INT_ADD =      10
MAX_INT_SUBTRACT = 10
MAX_INT_MULTIPLY = 10
MAX_INT_DIVIDE =   10


#-------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------
class BasicMath:
    """Basic mathematics class"""
    def __init__( self, function, symbol, maximum ):
        self.func = function
        self.sym = symbol
        self.max = maximum


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
    return a / b
    
    
#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
# Set various operations
add = BasicMath( math_func_add,      "+", MAX_INT_ADD      )
sub = BasicMath( math_func_subtract, "-", MAX_INT_SUBTRACT )
mul = BasicMath( math_func_multiply, "*", MAX_INT_MULTIPLY )
div = BasicMath( math_func_divide,   "/", MAX_INT_DIVIDE   )

# Set current math operation
math = add

# Continually ask arithmetic problems
while True:
    num1 = rand_get( math.max )
    num2 = rand_get( math.max )
    real_answer = math.func( num1, num2 )
    
    print num1,math.sym,num2,"= ?"
    
    # Get answer from user
    user_answer = user_input_get()
    
    if user_answer == real_answer:
        print "Correct, good job!"
    else:
        print "That's not right, good try. Here's the answer:"
        print num1,math.sym,num2,"=",real_answer
    
    print ""