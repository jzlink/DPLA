#!/usr/bin/env python

import string

alnumSet = set(string.letters +  string.digits)

thestring = "^*&@$" #test string since I can't get the 

testList = [
'', ' ', ' A', 'ahfhfnkf', '17364836', '!@#$%^', 'sbvj123$^&*'
]

#for string in testList:
#    print string

for string in testList:
    testString = string
    overlapSet = len(set(testString) &  alnumSet)

    if overlapSet > 0:
        print '%s is a string' %testString
    else:
        print ' %s is not a string' %testString

