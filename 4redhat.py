#!/usr/bin/python 

import re, sys
import getopt
import os.path 

class fetched:

    def __init__(self, line, regex, filename): 
        self.line_str = line
        self.regex_found = regex.string
	self.regex_start = regex.span()[0] + 1 
	self.filename = filename
        
        print 'Regex Found: ', self.regex_found
        # print 'self.line_str: ', self.line_str
        # print 'self.line_str = line ', line
        print 'Filename: ', filename

    # Define color blue for matched pattern. 
    # An alternative is to use the termcolor module, see: 
    # https://stackoverflow.com/questions/22886353/printing-colors-in-python-terminal
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'

    def print_plain(self): 
        to_print = self.filename + ':' + self.line_str
	print to_print 

    def colored(self):
        to_print = self.OKBLUE + self.line_str + self.ENDC
        print to_print

    def underscore(self):
        print self.line_str
        print ' ' * 10 + '^' * len(self.line_str)

    def machine_readable(self): 
        # Print following format: file_name:no_line:start_pos:matched_text
	# start_pos is the column number in the file. Assuming first column is column 1. 

        # to_print = self.filename + ':' + 'no_line_TBD' + ':' + 'start_pos_TBD' + ':' + self.regex_found
        # to_print = self.filename + ':' + self.regex_found
        to_print = str(self.regex_start) + ':' + self.regex_found
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
                print 'Matched at line: ', str(line_n) + ':' + line.strip()

                # 
                line_found = fetched(line, re.search(regex, line), f)
                if color: line_found.colored() 
                elif underscore: line_found.underscore()
                elif machine_format: line_found.machine_readable()
		else: line_found.print_plain() 

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
            print "color switch is ON" 
            color_on = True
            switches_on += 1 

        if opt in ('-u', '--underscore'): 
            print "underscore switch is ON" 
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

    if switches_on > 1: 
        print "Switches -c, -u and -m are mutually exclusive. Exiting"
        print "Please fix and rerun." 
        #sys.exit(3)
    
    grep_it(regex, file_list, color_on, underscore_on, machine_on) 


if __name__ == '__main__':
    main(sys.argv[1:])


