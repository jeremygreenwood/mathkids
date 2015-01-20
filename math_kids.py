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
# TODO add configurations:
#      * consider option to configure problem type for automatic selection based on the day of the week
#      * enable/disable negative numbers
#        if enabled, random number generation should be between (-max, max) as opposed to the normal (0, max)
#      * enable/disable remainders for division problems
# TODO consider adding parameters to override various configurations:
#      * how many math questions to perform (override configuration)
#      * others as needed
# TODO add learning functionality:
#      first need to implement database of problem history
#      if a question has been answered correctly many times it should be omitted
#      if too many questions are omitted then the maximum range value for the type of problem should be increased
# TODO add commands:
#       * help command to display a list of available commands and what they do


import platform
import random
from random import randrange
import sys
import os
import getopt
import datetime
import ConfigParser

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


#-------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------
# Colors
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

# Directory and filenames
USER_DIR_DFLT = "default"
CFG_FILE_DFLT = "config.ini"

# Configuration file defaults
NUM_PROBLEMS_DFLT     = 10
MAX_INT_ADD_DFLT      = 16
MAX_INT_SUBTRACT_DFLT = 8
MAX_INT_MULTIPLY_DFLT = 4
MAX_INT_DIVIDE_DFLT   = 2


#-------------------------------------------------------------------
# Classes
#-------------------------------------------------------------------
class BasicMath:
    '''
    Basic mathematics class, manages list of different types of math problems.
    '''
    # Subclass
    class MathType:
        '''
        Math problem type class, defines a type of math problem and its characteristics. This is used similar to a C struct.
        '''
        def __init__( self, function, generate, hint, symbol, maximum ):
            self.func = function
            self.gen  = generate
            self.hint = hint
            self.sym  = symbol
            self.max  = maximum
        
    def __init__( self ):
        self.problem_list = []
        
        # Setup/add various math problem types
        # TODO only setup enabled operators
        self.prob_add( BasicMath.MathType( BasicMath.add_func, BasicMath.add_gen_numbers, BasicMath.add_hint, "+", cfg_max_int_add ) )

        self.prob_add( BasicMath.MathType( BasicMath.sub_func, BasicMath.sub_gen_numbers, BasicMath.sub_hint, "-", cfg_max_int_subtract ) )
        
        self.prob_add( BasicMath.MathType( BasicMath.mul_func, BasicMath.mul_gen_numbers, BasicMath.mul_hint, "*", cfg_max_int_multiply ) )
        
        self.prob_add( BasicMath.MathType( BasicMath.div_func, BasicMath.div_gen_numbers, BasicMath.div_hint, "/", cfg_max_int_divide ) )
        
        
    def prob_add( self, problem ):
        self.problem_list.append( problem )
        
    def prob_gen( self, prob_type ):
        '''
        Generate a math problem
        '''
        # Generate random numbers for math problem
        self.num1, self.num2 = prob_type.gen( prob_type.max )
        
        # Compute the answer
        try:
            self.answer = prob_type.func( self.num1, self.num2 )
        except:
            print red( "An internal error occurred while computing the answer, setting answer to 0." )
            self.answer = 0
            
        self.question_str = str( self.num1 ) + " " + prob_type.sym + " " + str( self.num2 ) + " = ?"
        self.answer_str   = str( self.num1 ) + " " + prob_type.sym + " " + str( self.num2 ) + " = " + str( self.answer )
    
    def prob_hint( self ):
        '''
        Display a hint for the current math problem
        '''
        print self.current_problem.hint( self.num1, self.num2 )
            
    def prob_type_get( self ):
        '''
        Returns a random math problem type that is enabled
        '''
        self.current_problem = random.choice( self.problem_list )
        return self.current_problem
        
    @staticmethod
    def pluralize( word, num ):
        if num != 1:
            return word + "s"
        else:
            return word

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
    def add_hint( lhs, rhs ):
        item_type = "egg"
        lhs_items = BasicMath.pluralize( item_type, lhs )
            
        return "You have " + str( lhs ) + " " + lhs_items + " and get " + str( rhs ) + " more. How many " + item_type + "s?"
        
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
    def sub_hint( lhs, rhs ):
        item_type = "egg"
        lhs_items = BasicMath.pluralize( item_type, lhs )
            
        return "You have " + str( lhs ) + " " + lhs_items + " and lose " + str( rhs ) + ". How many " + item_type + "s?"
        
    @staticmethod
    def mul_func( a, b ):
        return a * b

    @staticmethod
    def mul_gen_numbers( maximum ):
        return ( BasicMath.rand_get( maximum ), BasicMath.rand_get( maximum ) )

    @staticmethod
    def mul_hint( lhs, rhs ):
        lhs_item_type = "basket"
        rhs_item_type = "egg"
        lhs_items = BasicMath.pluralize( lhs_item_type, lhs )
        rhs_items = BasicMath.pluralize( rhs_item_type, rhs )
        
        return "You have " + str( lhs ) + " " + lhs_items + " with " + str( rhs ) + " " + rhs_items + " in each " + lhs_item_type + ". How many " + rhs_item_type + "s?"
        
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

    @staticmethod
    def div_hint( lhs, rhs ):
        lhs_item_type = "egg"
        rhs_item_type = "pile"
        lhs_items = BasicMath.pluralize( lhs_item_type, lhs )
        rhs_items = BasicMath.pluralize( rhs_item_type, rhs )
            
        return "You have " + str( lhs ) + " " + lhs_items + " and need to split up into " + str( rhs ) + " equal " + rhs_items + ". How many " + lhs_item_type + "s in each " + rhs_item_type + "?"
        
        
class Game:
    '''    
    Math game class, keeps track of game statistics.
    '''
    def __init__( self, num_problems ):
        self.num_problems = num_problems
        self.prob_cnt     = 0
        self.correct_cnt  = 0
        self.math         = BasicMath()
        self.active       = True
        
    def stat_display( self, done ):
        '''
        Display statistics
        '''
        # If user entered the stat command display how many problems are remaining
        if done == False:
            num_prob_remaining = self.num_problems - self.prob_cnt
            print "Problems left: " + blue( str( num_prob_remaining ) )
        
        # Verify at least one problem has been done in order to display results
        if self.prob_cnt > 0:
    
            # Calculate the percentage of correct problems
            percent = int( 100 * float( self.correct_cnt ) / float( self.prob_cnt ) )
            
            print "Results:       " + blue( str( self.correct_cnt ) + "/" + str( self.prob_cnt ) + " correct (" + str( percent ) + "%)" )
    
            # If user is done print an encouraging message based on results
            if done == True:
                sys.stdout.write( "    " )
        
                if percent >= 100:
                    print "Perfect score!"
                elif percent >= 90:
                    print "Amazing job!"
                elif percent >= 80:
                    print "Great job!"
                elif percent >= 50:
                    print "Good job. You are doing well, and with practice will do even better!"
                else:
                    print "Good try. With practice you will do better, you can do it!"
        else:
            print "No results to display."

        # If user is done pause for user to see results before quitting
        if done == True:
            print blue( "\nPress Enter to quit" )
            raw_input()
            quit()
        
        
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
    
def user_input_get( game ):
    '''
    Get user input. First checks if the user entered a command to execute, otherwise attempts to return
    integer value to the calling application
    '''
    while True:
        try:
            user_input_str = raw_input( "Enter answer: " )
            
            # Check if the user wants to quit
            if ( user_input_str == "quit" ) or ( user_input_str == "exit" ):
                game.active = False
                return None
            # Check if the user wants a hint for the current problem
            elif user_input_str == "hint":
                game.math.prob_hint()
                continue
            # Check if the user wants to see statistics for the current game
            elif ( user_input_str == "stat" ) or ( user_input_str == "check" ) or ( user_input_str == "show" ):
                game.stat_display( done = False )
                continue
                
            return int( user_input_str )
        except ValueError:
            
            # Failed to get an integer from the user input, print a message and try again
            print yellow( "Answer not recognized." )
            pass
    
def usage():
    print "math_kids.py [options]"
    print "Option       Default value   Description"
    print " h                           Print this help message."
    print " u <user>    default         Set the user profile to use."
        
def cmd_opt_parse():
    '''
    Parse for command line options
    '''
    global username_dir
    
    opt_list = "hu:"
    try:
        opts, args = getopt.getopt( sys.argv[ 1: ], opt_list )
    except getopt.GetoptError as err:
        # Print help information and exit
        print str( err )
        usage()
        sys.exit( 2 )

    for o, a in opts:
        if o == "-h":
            usage()
            quit()
        elif o == "-u":
            username_dir = a
        else:
            assert False, "unhandled option"
            
def log_filename_gen():
    '''
    Return datetime log filename similar to ISO 8601 format
    '''
    return datetime.datetime.now().strftime( "%Y-%m-%dT%H_%M_%S.log" )
    

#-------------------------------------------------------------------
# Main
#-------------------------------------------------------------------
if __name__ == "__main__":
    
    # Set variables to default values
    username_dir = USER_DIR_DFLT
    cfg_file     = CFG_FILE_DFLT
    
    # Set default configurations
    # NOTE: most of these are currently referenced as globals in the class BasicMath
    cfg_number_of_problems  = NUM_PROBLEMS_DFLT
    cfg_max_int_add         = MAX_INT_ADD_DFLT
    cfg_max_int_subtract    = MAX_INT_SUBTRACT_DFLT
    cfg_max_int_multiply    = MAX_INT_MULTIPLY_DFLT
    cfg_max_int_divide      = MAX_INT_DIVIDE_DFLT
    cfg_add_enable          = True
    cfg_subtract_enable     = True
    cfg_multiply_enable     = True
    cfg_divide_enable       = True
    # Configs to implement
    cfg_negative_num_enable = False
    
    # Parse command line options
    # NOTE: this function assigns to global variables set above inside __main__
    cmd_opt_parse()
    
    # Create user directory if it does not exist
    if not os.path.exists( username_dir ):
        os.makedirs( username_dir )
        
    # Set config file path
    config_file_path = username_dir + "/" + cfg_file
    
    # Create config parser instance
    config = ConfigParser.ConfigParser()
        
    # Check if config file exists
    if not os.path.exists( config_file_path ):
        # Create config file contents
        config.set( 'DEFAULT', 'number_of_problems', str( cfg_number_of_problems ) )
        config.set( 'DEFAULT', 'add_enable',         str( cfg_add_enable ) )
        config.set( 'DEFAULT', 'subtract_enable',    str( cfg_subtract_enable ) )
        config.set( 'DEFAULT', 'multiply_enable',    str( cfg_multiply_enable ) )
        config.set( 'DEFAULT', 'divide_enable',      str( cfg_divide_enable ) )
        config.set( 'DEFAULT', 'max_int_add',        str( cfg_max_int_add ) )
        config.set( 'DEFAULT', 'max_int_subtract',   str( cfg_max_int_subtract ) )
        config.set( 'DEFAULT', 'max_int_multiply',   str( cfg_max_int_multiply ) )
        config.set( 'DEFAULT', 'max_int_divide',     str( cfg_max_int_divide ) )
        
        # Write the config file
        with open( config_file_path, 'w+' ) as configfile:
            config.write( configfile )
    else:
        # Read the config file
        config.read( config_file_path )
        cfg_number_of_problems = int( config.get( 'DEFAULT', 'number_of_problems' ) )
        cfg_add_enable = bool( config.get( 'DEFAULT', 'add_enable' ) )
        cfg_subtract_enable = bool( config.get( 'DEFAULT', 'subtract_enable' ) )
        cfg_multiply_enable = bool( config.get( 'DEFAULT', 'multiply_enable' ) )
        cfg_divide_enable = bool( config.get( 'DEFAULT', 'divide_enable' ) )
        cfg_max_int_add = int( config.get( 'DEFAULT', 'max_int_add' ) )
        cfg_max_int_subtract = int( config.get( 'DEFAULT', 'max_int_subtract' ) )
        cfg_max_int_multiply = int( config.get( 'DEFAULT', 'max_int_multiply' ) )
        cfg_max_int_divide = int( config.get( 'DEFAULT', 'max_int_divide' ) )
    
    # Set log file name name and path
    log_file_path = username_dir + "/" + log_filename_gen()
    
    # Create the log file and open for writing
    f = open( log_file_path, 'w+' )
    
    # Write the log file header
    f.write( "type,num1,num2,answer,correct?\n" )
    
    # Create a game instance with specified number of problems
    game = Game( cfg_number_of_problems )
    
    # Ask arithmetic problems for configured number of times
    while ( game.prob_cnt < game.num_problems ) and game.active:
        
        # Set current math operation randomly
        problem = game.math.prob_type_get()
        
        # Generate a math problem for the type of problem which was chosen randomly in the previous statement
        game.math.prob_gen( problem )
        
        # Print the math problem as a question
        print game.math.question_str
        
        # Get answer from user
        user_answer = user_input_get( game )

        # If no user input, retry the loop- this should fail if the game is no longer active
        if user_answer == None:
            continue
        
        # Print the calculated answer
        print "Answer: " + str( game.math.answer )
            
        # Print whether they got the math problem correct, and colorize accordingly
        if user_answer == game.math.answer:
            print green( "Correct" )
            game.correct_cnt += 1
            result_correct = "y"
        else:
            print red( "Not correct" )
            result_correct = "n"
            
        # Write the problem, answer, and result to the log file
        f.write \
            ( 
            game.math.current_problem.sym + "," + 
            str( game.math.num1 )         + "," + 
            str( game.math.num2 )         + "," + 
            str( user_answer )            + "," + 
            result_correct                + "\n"
            )
        
        # Flush the data to disk
        f.flush()
            
        print "---------------------------------------------------"
        
        game.prob_cnt += 1
        
    # Close the log file
    f.close()
    
    # Display game results
    game.stat_display( done = True )
