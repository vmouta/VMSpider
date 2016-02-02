#!/usr/bin/python
# vmspider
import os
import sys
import getopt
import linkedin
import showmeboone

from linkedin import LinkedIn

#globals
verbose = False
platforms = ["linkdin" , "showmeboone"]
platform = platforms[0]
output_file_name = None

login = None
password = None

query = None

#linkedin Globals
linkedin_country = None

def remove_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError, e:
            print ("Error: %s - %s." % (e.filename,e.strerror))
    else:
        print("Sorry, I can not find %s file." % filename)

# standard command line functions
def print_no_arguments(command):
    print("Usage: %s [OPTION]... [QUERY]" % command);
    print("Try '%s --help' for more information." % command);

def print_wrong_arguments(command, error):
    print(str(error));
    print("Try '%s --help' for more information." % command);

def print_help(command, platform):
    
    print("Usage: %s [OPTION]... [QUERY]" % command);
    print("  It fetch the list of the first 100 contacts for the query on the desired platform");
    
    print("\nExamples:");
    print("  \"./%s -v -q thequereyvalue -o result.cvs\"" % command);
    print("  \"./%s -v -p linkdin thequereyvalue\"" % command);
    print("  \"./%s -c pt -v Rent\"" % command);
    print("  \"./%s -c pt Rent >> out.csv" % command);
    print("  \"./%s -v thequereyvalue\"" % command);
    print("  \"cat in.txt | ./%s -\"" % command);
    
    print("\nOptions:");
    print("  -h, --help           - Help menu");
    print("  -v, --verbose        - For debugging");
    print("  -p, --platform       - [%s] Platform to fetch the contacts (Default:%s)" % (' | '.join(platforms), platform));
    print("  -q, --query          - The query string to be consider");
    print("  -l, --login          - Login to login on linkedin");
    print("  -r, --remove         - Delete cookie");
    print("  -w, --password       - Password to login on linkedin")
    print("  -,  --in             - Read query string from sys.stdin");
    print("  -o, --out            - Output file");
    print("\nLinkedIn platform Options:");
    print("      --listcountries  - Display the list of countries available for option \"-c\"");
    print("  -c, --country        - Set a sepecific country for fetch the contacts");

def print_values():
    print("----INPUT VALUES----")
    print("Verbose:%s" % verbose)
    print("Platform:%s" % platform)
    print("Outputfile:%s" % output_file_name)
    print("Query:%s" % query)
    print("Country:%s" % linkedin_country)
    print("--------")

def read_options(argn, argc, argv):
    try:
        opts, args = getopt.getopt(argv,"hvrc:p:l:w:o:q:",["help", "verbose", "remove", "listcountries", "country=", "platform=", "login=", "passoword=", "out=", "query=", "in"])
    except getopt.GetoptError as e:
        print_wrong_arguments(argn, e)
        sys.exit(2)

    optind = 0
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(argn, arg)
            sys.exit(0)
        elif opt == "--listcountries":
            print "\n".join(linkedin.countriesNameCode())
            sys.exit(0)
        elif opt in ("-v", "--verbose"):
            global verbose
            verbose = True
        elif opt in ("-r", "--remove"):
            remove_file("parser.cookies.txt")
        elif opt in ("-c", "--country"):
            global linkedin_country
            linkedin_country = arg
        elif opt in ("-o", "--out"):
            global output_file_name
            output_file_name = arg
        elif opt in ("-p", "--platform"):
            global platform
            if arg in platforms:
                platform = arg
            else:
                print("Platform \"%s\" not supported default \"%s\" will be used" % (arg, platform))
        elif opt in ("-l", "--login"):
            global login
            login = arg
        elif opt in ("-w", "--password"):
            global password
            password = arg
        elif opt == "--in":
            global query
            query = sys.stdin.readline().rstrip('\n')
        elif opt in ("-q", "--query"):
            query = arg
        optind = optind + 1 + (0 if arg == "" else 1)

    while optind < argc :
        if argv[optind] in ["-"] :
            query = sys.stdin.readline().rstrip('\n')
        elif query == None :
            query = argv[optind]
        optind = optind+1

    if verbose == True:
        print_values()

    #Main Action
    fetch = None
    if platform == 'linkdin':
        if login != None and password != None:
            fetch = LinkedIn(query, linkedin_country, verbose=verbose, login=login, password=password)
        else:
            fetch = LinkedIn(query, linkedin_country, verbose=verbose)
    elif x == 'showmeboone':
        fetch = ShowMeBoone()
    else:
        print("Upsssss, update needed")

    if verbose == True:
        print "Object Type - %s" % fetch

    # Fetch result
    fetch.csv(output_file_name)

# main command line function
def main(argn, argc, argv):
    
    #no arguments
    if argc == 0:
        print_no_arguments(argn)
        sys.exit(0)

    #fetch options
    read_options(argn, argc, argv)

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(sys.argv[0], len(argv), argv)

