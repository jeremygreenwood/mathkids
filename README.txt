mathkids
========

Description:
    Command line python script to help kids learn basic arithmetic.  Currently addition, subtraction, multiplication, and division
	are supported.	The program is easily configurable for multiple users with varying degrees of difficulty.
	
Usage:
	To test or use with the default user do one of the following:
		1. Run math_kids.py by double clicking (probably requires python be in your "PATH" environment variable)
		2. Run the following on the command line (cmd.exe for Windows users):
			python math_kids.py				(Windows)
			./math_kids.py					(Linux/Mac)
		3. Run math_kids.bat by double clicking (intended for Windows users)
	
	To setup for a specific user with configuration file do one of the following (example user being "Jane"):
		1. Run the following on the command line:
			python math_kids.py	-u Jane		(Windows)
			./math_kids.py -u Jane			(Linux/Mac)
		2. Create a shortcut with the target as one of the commands above and run by double clicking
		3. Modify math_kids.bat to contain the Windows command above and run by double clicking
		
	Once the program has successfully ran a user directory is created containing a configuration file "config.ini".
	Taking care, this file may be modified to change the user's default configuration.  The configuration will take effect
	the next time the program is run with the specified user.  This user directory is also where all logs will be saved 
	containing the results of all questions and answers.

Supported operating systems:
	Windows
	Linux
	Mac (untested but assumed compatible)
	*Mobile platforms (Android, iOS, etc) have not been tested and are assumed to not be compatible

Python version used during development:
    2.7.6

Required python packagse:
	None

Optional python packages:
    * colorama (Windows only) - Required for colorized output.  See below for installation information.

Features:
    * Math problem types: addition, subtraction, division, multiplication
    * Displays results on program end
    * The following commands are available on the answer prompt:
		hint:	Converts the numeric math problem to a word problem to make it easier for kids to grasp unfamiliar math operators
		show:	Display statistics of how many problems remain, and score for problems completed.
	* Running for a specific user.
    * Configuration file (config.ini) options:
        * Number of problems to quit after
        * Maximum random integer values for each math problem type
		* Enable or disable fore each math problem type
    * Colorized output using ANSI codes supported by Linux OS, and support for colorama on Windows OS
    * Logging of all answers
	
Potential features to add in the future:
    * Have the program increase the difficulty of the problems based on answer history
	* Add questions for math series (e.g. 2, 5, 8, ?, ?, ?)
	* Add negative number support (enable by configuration)
	* Add remainder support for division problems (enable by configuration) and provide answer as NrN (e.g. 5/3 = 1r2)
	* Add help command to print list of available commands on the answer prompt
	* Test and add support for mobile platforms with python support
	
To enable colored output on windows:
   1. Download colorama from https://pypi.python.org/packages/source/c/colorama/colorama-0.3.2.zip#md5=179cc70c4a61901ffd052576b598f11e
   2. Extract the downloaded zip file.
   3. Run the following commands in a windows terminal to install colorama:
	   python setup.py build
	   python setup.py install


You are welcome to email me with bugs, ideas, comments, questions, etc- see commit log for developer email address.
Thanks!
