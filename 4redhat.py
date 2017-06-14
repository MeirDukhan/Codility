#!/usr/bin/python 

import re, sys
import getopt
import os.path 

class fetched:


    def __init__(self, line, regex, filename, line_n): 
        self.line_str = line
	self.line_n = line_n
        #self.regex_found = regex.string
	#self.regex_start = regex.span()[0] + 1 
	#self.matched_text = regex.string[regex.span()[0]:regex.span()[1]]
	self.filename = filename
	self.regex_str = regex

    def print_plain(self): 
        to_print = self.filename + ':' + str(self.line_n) + ':' + self.line_str
	print to_print 

    def color_matches_in_line(self):
        '''
        Given a line and a string or regex matching at 'index', 
        Return a line with colored matches
        '''
	line = self.line_str
	regex_str = self.regex_str

        # Define color blue for matched pattern. 
        # An alternative is to use the termcolor module, see: 
        # https://stackoverflow.com/questions/22886353/printing-colors-in-python-terminal
	FOUND_COLOR = '\033[91m'
	ENDC = '\033[0m'
	
	# print 'Regex: ', regex
	colored_match = ''
	colored_line = ''
	for match in re.findall(regex_str, line):
	    match_len = len(match)
	    start_index = re.search(regex_str, line).span()[0] + 1
	    colored_line = line[:start_index-1] + FOUND_COLOR + match[:len(match)] + ENDC + line[start_index+len(match)-1:]
	print self.filename + ':' + str(self.line_n) + ':' + colored_line

    def underscore(self):
        # print self.line_str

	# Build the 'underscore' string for under the matching text
	# 
        # print ' ' * len(prefix_to_print) + '^' * len(self.line_str)

	# Find the position(s) of the matche(s) within the line 
	positions = list() 
	L = list(re.finditer(self.regex_str, self.line_str)) 
	for it in re.finditer(self.regex_str, self.line_str):
	    positions.append(it.span()) 

	# print 'Positions: ', positions
	# Initialize a list with the size of the line with single blanks 
	blanks = list([' '] * len(self.line_str)) 

	# Now, put the '^' in the place(s) of the matche(s) 
	for pos in positions: 
	    carets_to_put = pos[1] - pos[0] 
	    start_index_to_put_carets = pos[0]
	# print 'carets_to_put, start_index_to_put_carets: ', carets_to_put, start_index_to_put_carets

	for i in range(pos[0], pos[1]):
	    blanks[i] = '^' 
	i = 0
	line_with_underscore = ''
	while i < len(blanks):
	    line_with_underscore += blanks[i] 
	    i += 1 
	
	prefix_to_print = self.filename + ':' + str(self.line_n) + ':'

	print (prefix_to_print + self.line_str).strip()
	# print len(blanks), len(line_with_underscore) 
	# print 'Prefix + Line with underscore: ', prefix_to_print + line_with_underscore 
	print len(prefix_to_print) * ' ' + line_with_underscore 



    def machine_readable(self): 
        # Print following format: file_name:no_line:start_pos:matched_text
	# start_pos is the column number in the file. Assuming first column is column 1. 
	line = self.line_str
	regex_str = self.regex_str
	
	# print "Type of 'regex' object: ", type(regex_str) 
	r = re.search(regex_str, line)
	start_index = r.span()[0] + 1
	# print 'Start index: ', start_index

	matched_text = line[r.span()[0]:r.span()[1]]

        # to_print = self.filename + ':' + 'no_line_TBD' + ':' + 'start_pos_TBD' + ':' + self.regex_found
        # to_print = self.filename + ':' + self.regex_found
        # to_print = self.filename + ':' + str(self.regex_start) + ':' + self.regex_found
        to_print = self.filename + ':' + str(self.line_n) + ':' + str(start_index) + ':' + matched_text
	print to_print


def grep_it(regex, file_list, color=False, underscore=False, machine_format=False):
    '''
    str: regex
    list: file_list
    '''
    for f in file_list: 
        fh = open(f, 'r')
        line_n = 1
        for line in fh: 
            if re.search(regex, line):
                # print 'Matched at line: ', str(line_n) + ':' + line.strip()

                # 
                # line_found = fetched(line, re.search(regex, line), f)
                line_found = fetched(line, regex, f, line_n)

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
    list: flist
    ''' 
    flist_valid = [] 

    for f in flist:
        if os.path.isfile(f): 
            continue
        else: 
            print 'No such file: ', f
            flist_valid.append(f)

    return flist_valid


def main(argv):
    color_on = underscore_on = machine_on = False
    switches_on = 0                     # Counter for switches '-c', '-m', & '-u' 
    regex = None
    file_list = list()                  # To store the list of file(s) given in the command line

    # print "ARGV: ", argv

    try:
        opts, args = getopt.getopt(argv, "hcumr:f:", ["help", "color", "underscore", "machine", "regex=", "file="])
    except getopt.GetoptError:
        print "4redhat.py \
        -u, --underscore \
        -c, --color, highlight matching text \
        -m, machine, generate machine readable output with format: \
            file_name:no_line:start_pos:matched_text" 
        sys.exit(2)

    # print 'OPTS: ', opts 

    for opt, arg in opts: 
        if opt == '-h':
            print "4redhat.py -... "
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
            print "Generate machine readable input switch is ON" 
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
        print 'Output format: filename:line_number_for_match:line_matched\n\n' 
        
    if switches_on > 1: 
        print "Switches -c, -u and -m are mutually exclusive. Exiting"
        print "Please fix and rerun." 
        sys.exit(3)
    
    grep_it(regex, file_list, color_on, underscore_on, machine_on) 


if __name__ == '__main__':
    main(sys.argv[1:])


