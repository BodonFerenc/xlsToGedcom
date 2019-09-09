#!/usr/bin/python

import sys
from tableToGedcom import FamilyTreeMapping
import pyexcel as pe

def main(argv):
    # TODO consider using getopt
    if len(argv) < 4: 
        print("Four parameters are mandatory: input file, picture directory, first name and last name", file=sys.stderr)
        return
    t = pe.get_records(file_name=argv[0])
    ft = FamilyTreeMapping(t, argv[1])
    ft.printGedcom(argv[2], argv[3])

if __name__ == "__main__":
   main(sys.argv[1:])