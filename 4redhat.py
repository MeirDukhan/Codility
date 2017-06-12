#!/usr/bin/python 

import re, sys
import getopt
import os.path 

class fetched:
    line = 'Meir' 
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    def colored(self):
        # self.line = self.OKBLUE + 'Meir' + self.ENDC
        to_print = self.OKBLUE + self.line + self.ENDC
        print to_print

    def underscore(self):
        print 'Within underscore ' + self.line
        print ' ' * 10 + '^' * len(self.line)

    def machine_readable(self): 
        # Print following format: file_name:no_line:start_pos:matched_text
        print 'Within Machine readable ' + self.line

def grep_it(regex, file_list, color=False, underscore=False, machine=False):
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
                line_found = fetched() 
                line_found.colored() 

                line_found.underscore()
                line_found.machine_readable()

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
    
    grep_it(regex, file_list) 

if __name__ == '__main__':
    main(sys.argv[1:])

