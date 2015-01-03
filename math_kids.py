#!/usr/bin/python
#
# Notes:
#   To enable colored output on windows:
#       1. Download colorama from https://pypi.python.org/packages/source/c/colorama/colorama-0.3.2.zip#md5=179cc70c4a61901ffd052576b598f11e
#       2. Extract the downloaded zip file.
#       3. Run the following commands in a windows terminal to install colorama:
#           python setup.py build
#           python setup.py install
#
# TODO add usage statement
# TODO add parameters to only ask questions for add, sub, mult, div, random, or cycle through
#      consider option to configure for automatic selection based on the day of the week
# TODO add profiles to keep track of session logs and difficulty settings
#      may want to forgo profiles in favor of multiple installations
# TODO add logging of each session (and print a summary of results) to time-stamped file in a directory based on user profile
# TODO add learning functionality:
#      if a question has been answered correctly many times it should be omitted
#      if too many questions are omitted then the maximum range value for the type of problem should be increased
# TODO include configuration to enable negative numbers
#      this should effect the random number generation for subraction to ensure the answer is non-negative
#      if enabled, random number generation should be between (-max, max) as opposed to the normal (0, max)
# TODO add commands:
#       - should make the command or the first letter of the command active to run the command
#       * help command to display a list of available commands and what they do
#       * hint command to convert the math problem into a word problem for kids to conceptualize


import platform
import random
from random import randrange

# Try to import colorama for ANSI color if running Windows
color_enable = True
if platform.system() == "Windows":
    try:
        import colorama
        # Initialize colorama without stripping ANSI codes to resolve issue when running in spyder console
        # also see https://code.google.com/p/spyderlib/issues/detail?id=1917
        colorama.init( strip = False )
    except:
        # Disable color for windows without colorama
        print "Disabling color (colorama python module is required for Windows platforms)"
        color_enable = False
        pass


# Set configurations
# TODO read configs from a settings file, and use a default if the settings file DNE
MAX_INT_ADD      = 16
MAX_INT_SUBTRACT = 8
MAX_INT_MULTIPLY = 4
MAX_INT_DIVIDE   = 2

negative_num_enable = False


#-------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------
if color_enable == True:
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[36m'
    OFF    = '\033[0m'
else:
    RED    = ''
    GREEN  = ''
    YELLOW = ''
    BLUE   = ''
    OFF    = ''


#-------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------
class MathType:
    """Math problem type class, defines a type of math problem and its characteristics."""
    def __init__( self, function, generate, symbol, maximum ):
        self.func = function
        self.gen  = generate
        self.sym  = symbol
        self.max  = maximum
        self.enabled = False
        

# TODO can/should this be a subclass of MathType
class BasicMath:
    """Basic mathematics class, manages list of different types of math problems."""

    @staticmethod
    def rand_get( maximum ):
        return randrange( 0, maximum )
    
    @staticmethod
    def add_func( a, b ):
        return a + b

    @staticmethod
    def add_gen_numbers( maximum ):
        return ( BasicMath.rand_get( maximum ), BasicMath.rand_get( maximum ) )
        
    @staticmethod
    def sub_func( a, b ):
        return a - b

    @staticmethod
    def sub_gen_numbers( maximum ):
        num1 = BasicMath.rand_get( maximum )
        num2 = BasicMath.rand_get( maximum )
        
        if num1 > num2:
            lhs = num1
            rhs = num2
        else:
            lhs = num2
            rhs = num1
            
        return ( lhs, rhs )
        
    @staticmethod
    def mul_func( a, b ):
        return a * b

    @staticmethod
    def mul_gen_numbers( maximum ):
        return ( BasicMath.rand_get( maximum ), BasicMath.rand_get( maximum ) )
        
    @staticmethod
    def div_func( a, b ):
        return a / b

    @staticmethod
    def div_gen_numbers( maximum ):
        while True:
            lhs = BasicMath.rand_get( maximum )
            rhs = BasicMath.rand_get( maximum )
            
            # Avoid divide by zero
            if rhs == 0:
                continue
            
            # Avoid decimal results/remainders
            # TODO consider adding configuration to enable remainders and provide answer as NrN (e.g. 5/3 = 1r2)
            if float( lhs / rhs ) != float( lhs ) / float( rhs ):
                continue
                
            return ( lhs, rhs )

    def prob_add( self, problem ):
        self.problem_list.append( problem )
        
    def __init__( self ):
        self.problem_list = []
        
        # Set various operations
        add = MathType( BasicMath.add_func, BasicMath.add_gen_numbers, "+", MAX_INT_ADD      )
        sub = MathType( BasicMath.sub_func, BasicMath.sub_gen_numbers, "-", MAX_INT_SUBTRACT )
        mul = MathType( BasicMath.mul_func, BasicMath.mul_gen_numbers, "*", MAX_INT_MULTIPLY )
        div = MathType( BasicMath.div_func, BasicMath.div_gen_numbers, "/", MAX_INT_DIVIDE   )
        
        self.prob_add( add )
        self.prob_add( sub )
        self.prob_add( mul )
        self.prob_add( div )
        
    
    def prob_gen( self, prob_type ):
        #""""Generate a math problem""""
        # Generate random numbers for math problem
        self.num1, self.num2 = prob_type.gen( prob_type.max )
        
        # Compute the answer
        try:
            self.answer = prob_type.func( self.num1, self.num2 )
        except:
            # TODO consider logging this occurrence and the problem values
            print red( "An internal error occurred" )
            self.answer = 0
            
        self.question_str = str( self.num1 ) + " " + problem.sym + " " + str( self.num2 ) + " = ?"
        self.answer_str   = str( self.num1 ) + " " + problem.sym + " " + str( self.num2 ) + " = " + str( self.answer )
            
        
    def prob_type_get( self ):
        """Returns a random math problem type that is enabled"""
        # TODO this should cross reference with enabled variable of each MathType (unless problem list is changed to only contain enabled problems)
        return random.choice( self.problem_list )
        

#class MathKids(BasicMath):
#    """Main class for mathkids game"""
    

#-------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------
def green( text ):
    return GREEN + text + OFF

def red( text ):
    return RED + text + OFF

def yellow( text ):
    return YELLOW + text + OFF

def blue( text ):
    return BLUE + text + OFF

def user_input_get():
    while True:
        try:
            user_input_str = raw_input( "Enter answer: " )
            
            # Check if the user wants to quit
            # TODO process available commands here
            if user_input_str == "quit":
                print blue( "Exiting the program..." )
                quit()
                
            return int( user_input_str )
        except ValueError:
            
            # Failed to get an integer from the user input, print a message and try again
            print yellow( "Answer not recognized." )
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
    print basic_math.question_str
    
    # Get answer from user
    user_answer = user_input_get()
    
    # Print the calculated answer
    print "Answer: " + str( basic_math.answer )
        
    # Print whether they got the math problem correct, and colorize accordingly
    if user_answer == basic_math.answer:
        print green( "Correct" )
    else:
        print red( "Not correct" )
        
    print "---------------------------------------------------"
    