#!/usr/bin/env python

import yaml
import pprint
import collections #use collections.counter(list) for aggregating/counting
import string

from dpla_utils import * 
from Validator import *
from findDotString import find

class Profile(): 
    '''responsible for developing a profile for a given set of DPLA results. 
    in the future it will take a parameter determining the DPLA query
    currently queries are definded ad hoc in the constructor'''

    def __init__(self):
        #Julia's API from DPLA
        api_key = '2992771ce4f801b3c6ba94f38366c102'
        #Digital Libary of Georga collection key
        DLG_key = 'a72045095d4a687a170a4f300d8e0637'
        self.fields =  yaml.load(open('fields.yml', 'r'))
        self.DPLAData = dpla_fetch(api_key, 1, q= 'bicycle')
        self.validator = Validator()

    def createProfile(self):
        '''responsible for calling helper classes/methods and aggregating
        results. Returns a dictionary of CHO id's and their statuses
        '''
        #initialize collection dictionary, add DPLAfails to it. 
        # default DPLAfails to 0
        collection = {}
        collection['DPLAfails'] = 0
        #initialize dict to hold the items of a cho and their calculated grade
        CHO_items = {} 

        for CHO in self.DPLAData:
            DPLAfails = False
            # initialize dict to hold fields and their statuses
            field_list = {}

            for field in self.fields:
                #call the finder method
                fieldValue = find(field,CHO)

                #if the finder does not return false (it found something)
                # set present status to true and 
                # send the item to the validator set status accordingly
                if fieldValue != False:
                    self.fields[field]['present'] = True
                    fieldValid = self.validator.validate(fieldValue)
                    if fieldValid:
                        self.fields[field]['valid'] = True
                    else:
                        self.fields[field]['valid'] = False
                
                # if the finder returned false set present and valid statuses
                else:
                    self.fields[field]['present'] = False
                    self.fields[field]['valid'] = False

                #if any of the DPLA required fields are missing 
                #set DPLAfails to True
                if self.fields[field]['source'] == 'DPLA' and \
                   self.fields[field]['present'] == False:
                    DPLAfails = True
                    
                #append field and field status to field_list dict
                field_list[field] = self.fields[field]

            #increment DPLAfails if necessary
            if DPLAfails:
                collection['DPLAfails'] = collection['DPLAfails'] + 1

            #otherwise add field and statuses to CHO_items
            else:
                CHO_items[CHO['id']] = field_list
                
        return CHO_items

def test():
    test = Profile()
#    print test.DPLAData
    profile = test.createProfile()
#    pprint.pprint(test.fields)

#    pprint.pprint(test.DPLAData)
    pprint.pprint(profile)

if __name__ == '__main__':
    test()
