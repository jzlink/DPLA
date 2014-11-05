#!/usr/bin/env python

from dpla_utils import * 
import yaml

import pprint
import collections #use collections.counter(list) for aggregating/counting

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
        self.DPLAData = dpla_fetch(api_key, 10, q= 'bicycle')

    def sort(self):
        ##UNDER CONSTRUCTION - if checkes on recommended fields not present
        # otherwise operational
        '''given a set of data from dpla sort each items fields into
        required, recommended, and DPLA required fileds. Return a dictionary
        of lists of present and missing fields'''

        #will hold a dict of items and their associated sorted fields
        sortedFields = {}
        # will count number of records DPLA fails to provide its DPLA required 
        #fields for. Anticipating it will remain 0.
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

                #identify DPLA required fields
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

            #check if conditional recommended fields are present
            for field in self.fields['if']:
                sub_field = self.fields['if'][field]
                if field in recommended:
                    #special handeling for collection sub_fields
                    if field == 'collection':
                        for sub_field in self.fields['if'][field]:
                            c_field = 'collection.%s' %sub_field
                            if sub_field in CHO['sourceResource'][field]:
                                recommended.append(c_field)
                            else:
                                missing_recommended.append(c_field)

                    else:
                        #find out what SR sub_field each thing is
                        #adjust CHO index accordingly
                        field_type = type(CHO['sourceResource'][field])
                        check_field = ''
                        if field_type == list:
                            check_field = CHO['sourceResource'][field][0]
                        else:
                            check_field = CHO['sourceResource'][field]
                            
                        #put it all together and check for conditional field
                        if sub_field not in check_field:
                            recommended.remove(field)
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
                compiled['missing_recommended'] = missing_recommended

                sortedFields[CHO['id']] = compiled

            else:
                fails = fails + 1
                sortedFields['fails'] = fails 

        return sortedFields

    def validate(self, dic):
        ''' accepts dics of items with lists of their sorted fields
        matches a full CHO record in DPLAData to each item, validates data
        returns an updated sorted dict reflecting validity checks'''
            ##UNDER CONSTRUCTION CAUTION PSEUDO CODE

            # for each item in the sorted dict match item to full CHO record
            # from DPLA
        for item in dic:
            for CHO in self.DPLAData:
                if CHO['id'] == item:
                    record = CHO

            #for each matched CHO record validate fields in self.fields
            #for field in self.fields['required_SR']:
            #    validate record[field] valid
                

def test():
    test = Profile()
    sortedFields = test.sort()
#    validated = test.validate(sortedFields)

#    pprint.pprint(test.DPLAData)
    pprint.pprint(sortedFields)
   # print validated
   

if __name__ == '__main__':
    test()
