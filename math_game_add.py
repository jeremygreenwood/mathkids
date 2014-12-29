#!/usr/bin/python
# TODO create library functions to make the high level parts of the program very easy for kids to read
# TODO add usage statement
# TODO add colorizing: green when correct, red when incorrect
# TODO add functionality for subtraction, multiplication, and division
# TODO add parameters to only ask questions for add, sub, mult, div, random, or cycle through
#      perhaps have option to configure for automatic selection based on the day of the week
# TODO add profiles to keep track of session logs and difficulty settings
# TODO add logging of each session (and print a summary of results) to time-stamped file in a directory based on user profile
# TODO add learning functionality:
#      if a question has been answered correctly many times it should be omitted
#      if too many questions are omitted then the maximum range value for the type of problem should be increased


from random import randrange

RAND_RANGE=10

def rand_get():
	return randrange( 0, RAND_RANGE )
    
    
while True:
	num1 = rand_get()
	num2 = rand_get()
	real_answer = num1 + num2
    
	print num1,"+",num2,"= ?"
    
	# Get answer from user
	# TODO handle invalid number
	user_answer = int( raw_input( "Enter answer: " ) )
    
	if user_answer == real_answer:
		print "Correct, good job!"
	else:
		print "That's not right, good try. Here's the answer:"
		print num1,"+",num2,"=",real_answer
		
	print ""