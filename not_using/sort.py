#!/usr/bin/env python

from dpla_utils import * 

import pprint
import collections
import yaml


class Profile(): 

    def __init__(self):
        #Julia's API from DPLA
        self.api_key = '2992771ce4f801b3c6ba94f38366c102'
        col_key = 'a72045095d4a687a170a4f300d8e0637'
        self.fields =  yaml.load(open('fields.yml', 'r'))
        self.DPLAData = dpla_fetch(self.api_key, 2, q= 'bicycle')

    def sort(self):
        ##UNDER CONSTRUCTION
        '''given a set of data from dpla sort each items fields into
        required, recommended, and DPLA required fileds. Return a dictionary
        of lists of present and missing fields'''

        #will hold a dict of items and their associated sorted fields
        sortedFields = {}
        fails = 0
        sortedFields['fails'] = fails

        for CHO in self.DPLAData:
            general_keys = [] #will hold keys from non SR items
            SR_keys = [] #will hold keys from SR items
            DPLA = [] #list of present DPLA required fields
            required_general = [] #list of present required general fields
            required_SR = [] #list of present required SR fields
            recommended = []  #list of present recommended fields 
            missing_general = [] #list of missing general fields
            missing_SR = [] # list of missing SR fields
            missing_recommended= [] # list of missing recommended fields

            #get the fields present at the doc level
            for field in CHO:
                general_keys.append(field)

                #find DPLA required fields
                if field in self.fields['DPLA']:
                    DPLA.append(field)

            #get the fields present at the SR level
            for field in CHO['sourceResource']:
                SR_keys.append(field)

            #sort present/missing general fields
            for field in self.fields['required_general']:
                if field in general_keys:
                    required_general.append(field)
                else:
                    missing_general.append(field)

            #sort present/missing SR fields
            for field in self.fields['required_SR']:
                if field in SR_keys:
                    required_SR.append(field)
                else:
                    missing_SR.append(field)

            #sort present/missing recommended fields:
            for field in self.fields['recommended']:
                if field in SR_keys:
                    recommended.append(field)
                else:
                    missing_recommended.append(field)
                
            #if all required DPLA fields are present compile lists and
            # return dict of items with lists of sorted fileds
            #otherwise increment number of failures in the dict. 
            if len(DPLA) == len(self.fields['DPLA']):
                compiled = {}
                compiled['required_general'] = required_general
                compiled['required_SR'] = required_SR
                compiled['recommended'] = recommended
                compiled['missing_general'] = missing_general
                compiled['missing_SR'] = missing_SR

                sortedFields[CHO['id']] = compiled

            else:
                fails = fails + 1
                sortedFields['fails'] = fails 

        return sortedFields

def test():
    test = Profile()
    sortedFields = test.sort()

#    pprint.pprint(test.DPLAData)
#    print len(test.DPLAData[0]['sourceResource'])
    pprint.pprint(sortedFields)
#    print SRcount
#    print doccount


if __name__ == '__main__':
    test()


        
