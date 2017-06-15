#!/usr/bin/python 

# RedHat assignment. Given on June 11, afternoon.
# Reference: Ofer Blaut (Hiring manager), Edita Aharonovich, RedHat
#
# Implement a script in Python that searches one or more named input
# files (standard input if no files are specified, or the file name
# '-' is given) for lines containing a match to a regular expression
# pattern (given on command line as well).
#
# Assume that input is ascii, you don't need to deal with different
# encoding.
#
# If a line matches, print it. Please print the file name and the line
# number for every match.
#
# Script accept list optional parameters which are mutually exclusive:
# -u ( --underscore ) which prints '^' under the matching text
# -c ( --color ) which highlight matching text [1]
# -m ( --machine ) which generate machine readable output
#                   format: file_name:no_line:start_pos:matched_text
#
# Multiple matches on single line are allowed, without overlapping.
#
# The script should be compatible with Python 2.6, and in line with
# PEP8 coding guidelines. Please add proper documentation and error
# handling.
#
# Hint: It is recommended to use a module for parsing the command line
# arguments and the "re" module for matching the pattern.
#
# Try to use OOP in order to encapsulate differences  between output
# formats. Please put into comments what design pattern it follows.
#
# Feel free to ask any questions you have.
#
# [1] http://www.pixelbeat.org/docs/terminal_colours

# Name:		redhat_assignmenti_June2017.py 
# Purpose:	A grep-like script 
# Author:	Meir Dukhan, mdukhan2@gmail.com 
# Created: 	June 12, 2017
# 

import re, sys
import getopt
import os.path 

class MatchedLine:

    def __init__(self, line, regex, filename, line_n): 
        self.line_str = line
	self.line_n = line_n
	self.filename = filename
	self.regex_str = regex

    def print_plain(self): 

        to_print = self.filename + ':' + str(self.line_n) + ':' + self.line_str
	print to_print.strip()

    def color_matches_in_line(self):
        """ 
        Return a line with colored matches, given a line and a string of regex. 

	Limitations: non-recursive, so it will color only the first match in line.
        """
	line = self.line_str
	regex_str = self.regex_str

        # Define color blue for matched pattern. 
        # An alternative is to use the termcolor module, see: 
        # https://stackoverflow.com/questions/22886353/printing-colors-in-python-terminal
	FOUND_COLOR = '\033[91m'
	ENDC = '\033[0m'
	
	# Build the colored line
	colored_line = ''
	for match in re.findall(regex_str, line):
	    match_len = len(match)
	    start_index = re.search(regex_str, line).span()[0] + 1
	    colored_line = line[:start_index-1] + FOUND_COLOR + match[:len(match)] + ENDC + line[start_index+len(match)-1:]

	# Print the colored line following format: <filename>:<line number>:<line with highlighted match(es)> 
	print (self.filename + ':' + str(self.line_n) + ':' + colored_line).strip()

    def underscore(self):
	""" 
	Print match(es) of a regex within a line along with a 'underscore' string under the matching text. 

	The idea is to build a string of ' ' with the length of the matching line and fill the positions 
	of the matching with '^'. 
	Then print the matching line and the line with spaces (' ') and carets ('^') below it. 

	LIMITATIONS: 
		1. does not work as expected with text files containing tabs in the matched lines.
		2. only underscore the last match in a line
	""" 

	# Find the position(s) of the match(es) within the line 
	positions = list() 
	L = list(re.finditer(self.regex_str, self.line_str)) 
	for it in re.finditer(self.regex_str, self.line_str):
	    positions.append(it.span()) 

	# Initialize a list with the size of the line with single blanks. 
	# (Using a list to be able to change its content. Then, build a string from it. 
	blanks = list([' '] * len(self.line_str)) 

	# Now, put the '^' in the place(s) of the matche(s) 
	for pos in positions: 
	    carets_to_put = pos[1] - pos[0] 
	    start_index_to_put_carets = pos[0]

	for i in range(pos[0], pos[1]):
	    blanks[i] = '^' 
	i = 0
	line_with_underscore = ''
	while i < len(blanks):
	    line_with_underscore += blanks[i] 
	    i += 1 
	
	# Build prefix following pattern: '<filename>:<line number>:' 
	prefix_to_print = self.filename + ':' + str(self.line_n) + ':'

	# Print matched line and then the 'underscored' string
	print (prefix_to_print + self.line_str).strip()

	# Now, print spaces with length of the prefix added by the line with the underscores ('^') 
	print len(prefix_to_print) * ' ' + line_with_underscore


    def machine_readable(self): 
    	""" 
        Print following format: <file_name>:<no_line>:<start_pos>:<matched_text> 
	start_pos is the column number in the file. 
	Assuming first column is column 1. 
	""" 
	line = self.line_str
	regex_str = self.regex_str
	
	# print "Type of 'regex' object: ", type(regex_str) 
	r = re.search(regex_str, line)
	start_index = r.span()[0] + 1
	# print 'Start index: ', start_index

	matched_text = line[r.span()[0]:r.span()[1]]

        to_print = self.filename + ':' + str(self.line_n) + ':' + str(start_index) + ':' + matched_text
	print to_print


def grep_it(regex, file_list, color=False, underscore=False, machine_format=False):
    '''
    :param regex: A regex expression
    :type str
    :param file_list: A list of existing file(s) 
    :type list
    '''
    for f in file_list: 
        fh = open(f, 'r')
        line_n = 1
        for line in fh: 
            if re.search(regex, line):
                # print 'Matched at line: ', str(line_n) + ':' + line.strip()

                # 
                line_found = MatchedLine(line, regex, f, line_n)

                # if color: line_found.colored() 
                if color: line_found.color_matches_in_line()
                elif underscore: line_found.underscore()
                elif machine_format: line_found.machine_readable()
		else: 
		    # print 'Print format: filename:line_number_for_match:line_matched\n\n' 
		    line_found.print_plain() 

            line_n += 1

def check_files(flist):
    '''
    Check if file(s) exists and is/are accessible
    :param flist: A list of filenames 
    :type list
    ''' 
    flist_valid = [] 

    for f in flist:
        if os.path.isfile(f): 
            continue
        else: 
            print 'No such file: ', f
            flist_valid.append(f)

    return flist_valid

def usage():
    print 'Usage: 4redhat.py \n' \
	'     -h, --help,         Print this help message\n' \
	'     -c, --color,        Highlight matching text\n' \
	'     -u, --underscore,   Print "^" under the matching text\n' \
	'     -m, --machine       Print in machine format: file_name:no_line:start_pos:matched_text\n'

def main(argv):
    color_on = underscore_on = machine_on = False
    switches_on = 0                     # Counter for switches '-c', '-m', & '-u' 
    regex = None
    file_list = list()                  # To store the list of file(s) given in the command line

    # print "ARGV: ", argv

    try:
        opts, args = getopt.getopt(argv, "hcumr:f:", ["help", "color", "underscore", "machine", "regex=", "file="])
    except getopt.GetoptError:
	usage()
        sys.exit(2)

    # print 'OPTS: ', opts 

    for opt, arg in opts: 
        if opt == '-h':
            usage()
            sys.exit()

        if opt in ('-c', '--color'): 
            # print "color switch is ON" 
            print 'Output format: filename:line_number_for_match:line_matched. Matched pattern in red\n\n' 
            color_on = True
            switches_on += 1 

        if opt in ('-u', '--underscore'): 
            # print "underscore switch is ON" 
            underscore_on = True
            switches_on += 1 

        if opt in ('-m', '--machine'):
            print "Generate machine readable output"
            print "\tfile_name:no_line:start_pos:matched_text\n"
            machine_on = True
            switches_on += 1 
        
        if opt in ('-r', '--regex'):
            regex = arg
            # print "Regex: ", regex 

        if opt in ('-f', '--file'):
            # print "opt: ", opt, 'arg', arg
            # Build a file list from the file(s) specified in the command line
            file_list.append(arg)

            # Check that file(s) exists and we can open it/them
            if len(file_list) is not 0: 
                check_files(file_list)

    # print "File list:", file_list
    if switches_on == 0: 
        print 'Output format: filename:line_number_for_match:line_matched\n' 
        
    if switches_on > 1: 
        print "Switches -c, -u and -m are mutually exclusive. Exiting"
        print "Please fix and rerun." 
        sys.exit(3)
    
    grep_it(regex, file_list, color_on, underscore_on, machine_on) 


if __name__ == '__main__':
    main(sys.argv[1:])


