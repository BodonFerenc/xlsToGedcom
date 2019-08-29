#!/usr/bin/python

import sys
from tableToGedcom import FamilyTreeMapping
import pyexcel as pe

def main(argv):
    t= pe.get_records(file_name=sys.argv[1])
    ft = FamilyTreeMapping(t, sys.argv[2])
    ft.printGedcom(sys.argv[3], sys.argv[4])

if __name__ == "__main__":
   main(sys.argv[1:])    