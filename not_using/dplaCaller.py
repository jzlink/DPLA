#!/usr/bin/env python

import pprint
from dpla_utils import * 

def types():
    #Julia's API from DPLA
    api_key = '2992771ce4f801b3c6ba94f38366c102'
    col_key = '3f0e282f7fed21d7790fce877faf11d7'
    #use  Madhurah's dpla_fetch to get 10 items containing 'kitten'
    results = dpla_fetch(api_key, 1, q= col_key)

    pprint.pprint(results) # <-- uncomment this line if you just want to print results 

#    for thing in results:
#        do something

#        print something

    #print a message telling us what variable types we get as results 
    print "Results is a "
    print type(results)
    print "Items in results are: "
    for item in results:
        print type(item)

#special thing that runs if this code is called at the command line. 
#call at the command line by typing ./<filepath/types.py> 
#  or ./types.py if in this dir.

if __name__ == '__main__':
    types()
    
