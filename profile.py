#!/usr/bin/env python


import pprint
import collections
import string
from copy import copy, deepcopy
import json

import yaml

from dpla_utils import dpla_fetch 
from integrity import *
from dotstring import find
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
#        self.DPLAData = createTestCollection()
        self.DPLAData = dpla_fetch(api_key, 10, q= 'bicycle')
        self.integrity = Integrity()
        self.collectionFields = {}
        for field in self.fields:
            self.collectionFields[field] = []

    def create_profile(self):
        '''responsible for calling helper classes/methods and
        aggregating results. Returns a dictionary of CHO id's and each
        of their field information as well as field status counts
        aggregated accross the collection
        '''

        collection = {}
        items = {}

        for CHO in self.DPLAData:
            #For each item in the collection open a blank metadata form.
            fieldMetadata =  yaml.load(open('fields.yml', 'r'))

            #For each feld of interest in the shema check if it is
            #found in the item.
            for field in fieldMetadata:
                #Call the finder method
                fieldValue = find(field,CHO)

                #If the field was not found assign False to the 
                # 'present' metadata element.           
                if fieldValue == False:
                    fieldMetadata[field]['present'] = False

                #Otherwise set the element 'present' to true
                # and check if the field is empy or not.
                else:
                    fieldMetadata[field]['present'] = True
                    if len(fieldValue) > 0:
                        fieldMetadata[field]['empty'] = False
                        #If the field is not empty check the integrity
                        # set metadata elements accordingly.
                        integrity = self.integrity.validate(fieldValue)
                        if integrity:
                            fieldMetadata[field]['integrity'] = True
                        else:
                            fieldMetadata[field]['integrity'] = False
                        
                    else:
                        fieldMetadata[field]['empty'] = True        

            #Send all field metadata to stauts assigner 
            fieldMetadata = self.assign_field_status(fieldMetadata)

            #Add the item id and the field metadata to the 'items' dict
            items[CHO['id']] = fieldMetadata
            
        #Aggregate collection statuses held in self.collectionFields
        aggFields = self.aggregate_fields(self.collectionFields)

        #Add all items to collection dictionary
        collection['items'] = items
        #Add aggregated field counts to the collection dictionary
        collection['aggregated field counts'] = aggFields 

        #Convert collection dictoinary to standard JSON format
        collection = json.dumps(collection)

        return collection

    def assign_field_status(self, fieldMetadata):
        '''Accepts a dictionary of metadata about each field of
        interest in a given DPLA item. Returns the same dictionary
        with one of 8 statuses assgined to each field.
        '''
        for field in fieldMetadata:
            #Initialize all statuses to 00
            status = 00

            #Divide fields into present and missing
            if fieldMetadata[field]['present'] == True:
                status = 2
            else:
                status = 1

            #If a field has a missing status check if its parent field
            # is also missing. If it is re-assign the child field's 
            # status.
            if status == 1 and \
               'conditional parent field' in fieldMetadata[field]:

                parent = fieldMetadata[field]['conditional parent field']
                if fieldMetadata[parent]['present'] == False:
                    status = 5

            #If the field has a present status check if it is empty
            # and re-assign status if necessary.
            if status == 2 and fieldMetadata[field]['empty'] == True:
                status = 3

            #If the field has a present status check if it has
            # integrity and re-assign status if necessary.
            if status == 2 and fieldMetadata[field]['integrity'] == False:
                status = 4

            #If the field is not missing and it has a conditional sub
            # field check the status of its sub field, re-assign
            # status if necessary.
            if status != 1 and\
               'conditional sub-field' in fieldMetadata[field]:
               
                child = fieldMetadata[field]['conditional sub-field']

                if fieldMetadata[child]['present'] == False:
                    status = 6
                if fieldMetadata[child]['empty']== True:
                    status = 7
                if fieldMetadata[child]['integrity'] == False:
                    status = 8

            #Set field status in metadata
            fieldMetadata[field]['status'] = status

            #Add status to collection level group of field statuses
            self.collectionFields[field].append(status)

        return fieldMetadata

    def aggregate_fields(self, fieldDict):
        '''Accepts a dictionary of fields and each status that field
        ever holds counts the field status by field and returns a
        dictonary of tallied statuses
        '''
        aggregatedFieldCounts = {}
        for field in fieldDict:
            tallyDict = {}
            #Count number of individual statuses assigned to each field
            status_count = collections.Counter(fieldDict[field])
            
            #Stat will be a number.
            #For each number look up the text of its status in the
            # fieldStat dict change the number to text value in the
            # final dict.
            for stat in status_count:
                status = self.fieldStat[stat]
                tallyDict[status] = status_count[stat]

            #Add aggregated status counts by field to final dict 
            aggregatedFieldCounts[field] = tallyDict

        return aggregatedFieldCounts




def test():
    test = Profile()
    profile = test.create_profile()
    print profile
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



