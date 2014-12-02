#!/usr/bin/env python

import yaml
import pprint
import collections #use collections.counter(list) for aggregating/counting
import string
from copy import copy, deepcopy
import json

from dpla_utils import * 
from isAlphaNum import *
from findDotString import find
from testCollection import createTestCollection

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
        self.fieldStat = yaml.load(open('fieldStatus.yml', 'r'))
        self.DPLAData = createTestCollection()
#        self.DPLAData = dpla_fetch(api_key, 10, q= 'bicycle')
        self.isAlphaNum = IsAlphaNum()
        self.collectionFields = {}
        for field in self.fields:
            self.collectionFields[field] = []

    def createProfile(self):
        '''responsible for calling helper classes/methods and aggregating
        results. Returns a dictionary of CHO id's and their statuses
        '''
        #initialize dict to hold each document in a collection, 
        # its field's statuses and grade  
        collection = {}
        items = {}

        for CHO in self.DPLAData:
            fieldMetadata =  yaml.load(open('fields.yml', 'r'))
#            fieldMetadata = copy(self.fields)
#            fieldMetadata = deepcopy(self.fields)
            for field in fieldMetadata:
                #call the finder method
                fieldValue = find(field,CHO)
            
                if fieldValue == False:
                    fieldMetadata[field]['present'] = False

                else:
                    fieldMetadata[field]['present'] = CHO['id']
                    if len(fieldValue) > 0:
                        fieldMetadata[field]['empty'] = False
                        alphaNum = self.isAlphaNum.validate(fieldValue)
                        if alphaNum:
                            fieldMetadata[field]['alphanumeric'] = True
                        else:
                            fieldMetadata[field]['alphanumeric'] = False
                        
                    else:
                        fieldMetadata[field]['empty'] = True                                
            fieldMetadata = self.assign_field_status(fieldMetadata)

            items[CHO['id']] = fieldMetadata
            
        aggFields = self.aggregate_fields(self.collectionFields)
        collection['items'] = items
        collection['aggregated field counts'] = aggFields 
#        collection = json.dumps(collection)
        return collection

    def assign_field_status(self, fieldMetadata):
        for field in fieldMetadata:
            status = 00
            #divide fields into present and missing
            if fieldMetadata[field]['present'] == True:
                status = 2
            else:
                status = 1

            if status == 1 and \
               'conditional parent field' in fieldMetadata[field]:
                parent = fieldMetadata[field]['conditional parent field']
                if fieldMetadata[parent]['present'] == False:
                    status = 5

            if status == 2 and fieldMetadata[field]['empty'] == True:
                status = 3

            if status == 2 and fieldMetadata[field]['alphanumeric'] == False:
                status = 4

            if status != 1 and\
               'conditional sub-field' in fieldMetadata[field]:
                child = fieldMetadata[field]['conditional sub-field']

                if fieldMetadata[child]['present'] == False:
                    status = 6
                if fieldMetadata[child]['empty']== True:
                    status = 7
                if fieldMetadata[child]['alphanumeric'] == False:
                    status = 8

            #set field status
            fieldMetadata[field]['status'] = status
            self.collectionFields[field].append(status)

        return fieldMetadata

    def aggregate_fields(self, fieldDict):
        aggregatedFieldCounts = {}
        for field in fieldDict:
            tallyDict = {}
            stat_count = collections.Counter(fieldDict[field])
            for stat in stat_count:
                status = self.fieldStat[stat]
                tallyDict[status] = stat_count[stat]
            aggregatedFieldCounts[field] = tallyDict

        return aggregatedFieldCounts




def test():
    test = Profile()
    profile = test.createProfile()
    for item in profile['items']:
        print item
        for sub-item in profile['items'][item]:
            print sub-item
#        print profile['items'][item]['present']


#    print profile
#    print profile['aggregated field counts']
#    agg = test.aggregate_fields(test.collectionFields)
#    print test.collectionFields
#    pprint.pprint(test.DPLAData)
#    pprint.pprint(profile)


if __name__ == '__main__':
    test()



#    for item in profile:
#        print item
#        for field in profile[item]:
#            print '%s: Present  %s Status %s' %(field, profile[item][field]['present'], profile[item][field]['status'])



