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
        self.fieldStat = yaml.load(open('fieldStatus.yml', 'r'))
        self.DPLAData = dpla_fetch(api_key, 10, q= 'bicycle')
        self.validator = Validator()

    def createProfile(self):
        '''responsible for calling helper classes/methods and aggregating
        results. Returns a dictionary of CHO id's and their statuses
        '''
        #initialize dict to hold each document in a collection, 
        # its field's statuses and grade  
        collection = {} 

        for CHO in self.DPLAData:
            fieldMetadata = self.fields.copy()

            for field in fieldMetadata:
                #call the finder method
                fieldValue = find(field,CHO)

                #if the finder does not return false (it found something)
                # set present status to true and 
                # send the item to the validator set status accordingly
                if fieldValue != False:
                    fieldMetadata[field]['present'] = True
                    if len(fieldValue) > 0:
                        fieldMetadata[field]['empty'] = False
                        fieldValid = self.validator.validate(fieldValue)
                        if fieldValid:
                            fieldMetadata[field]['valid'] = True
                        else:
                            fieldMetadata[field]['valid'] = False
                    else: 
                        fieldMetadata[field]['empty'] = True    
                        fieldMetadata[field]['alphanumeric'] = False
                    
                # if the finder returned false set present and valid statuses
                else:
                    fieldMetadata[field]['present'] = False
                    fieldMetadata[field]['empty'] = True                    
                    fieldMetadata[field]['alphanumeric'] = False

            #send field metadata to field status assigner
            fieldMetadata = self.assign_field_status(fieldMetadata) 

            #check if the DPLA has ever Failed
            DPLAFails = 0
            if fieldMetadata[field]['source'] == 'DPLA' and\
                          fieldMetadata[field]['stauts'] != 2:
                DPLAFails += 1

            #otherwise add field and statuses to CHO_items
            else:
                collection[CHO['id']] = fieldMetadata
                
            collection['DPLAFails'] = DPLAFails

        return collection

    def assign_field_status(self, fieldMetadata):
        for field in fieldMetadata:
            status = 00
            #divide fields into present and missing
            if fieldMetadata[field]['present'] == True:
                status = 2
            else:
                status = 1

            #check if a present field is valid or invalid
            if status == 2 and fieldMetadata[field]['alphanumeric'] == False:
                status = 3
 
            #check if a present field has conditional sub-fields
            if status == 2 and \
                           'conditional sub-fields' in fieldMetadata[field]:
                subField = fieldMetadata[field]['conditional sub-fields']
                #adjust status if sub-field missing or invalid
                if fieldMetadata[subField]['present'] == False:
                    status = 5
                if fieldMetadata[subField]['present'] == True and\
                   fieldMetadata[subField]['alphanumeric'] == False:
                    status = 6
            
            #check if a field is missing because its parent field is missing
            if status == 1 and\
                           'conditional parent-field' in fieldMetadata[field]:
                parent = fieldMetadata[field]['conditional parent-field']
                if fieldMetadata[parent]['present'] == False:
                    status = 4
            
            #set field status
            fieldMetadata[field]['status'] = status

        return fieldMetadata

    def assign_CHO_grade(self, fieldMetadata):
        field_num = len(fieldMetadata)
        valid_field_num = 0
        statuses = []
        grade = 99
        for field in fieldMetadata:
            if fieldMetadata[field]['source'] == 'DPLA' and\
               fieldMetadata[field]['status'] !=2:
                field_num = field_num -1
            
            if fieldMetadata[field]['required'] == 1 and \
               fieldMetadata[field]['status'] !=2:
                grade = 0
            
            else:
                statuses.append(fieldMetadata[field]['status'])
                
            for number in statuses:
                if number == 2:
                    valid_field_num +=1

            grade = float((valid_field_num)/(field_num))

        return grade
                

def test():
    test = Profile()
    profile = test.createProfile()
    pprint.pprint(profile)
#    print len(profile)
#    print len(test.fields)
#    for idnum in profile:
#        if idnum != 'DPLAFails':
#            print test.assign_CHO_grade(profile[idnum])
#            for field in profile[idnum]:
#                print profile[idnum][field]['status']



if __name__ == '__main__':
    test()


#
#
#    fieldMD = test.fields
#    fieldstat = test.assign_field_status(fieldMD)
#    print test.DPLAData
#    pprint.pprint(test.fields)
#    pprint.pprint(test.DPLAData)
#    pprint.pprint(fieldstat)
#    for idnum in profile:
#        if idnum !='DPLAFails':
#            for field in profile[idnum]:
#                if profile[idnum][field]['source'] == 'DPLA':
#                    print 'DPLA'
#                    print profile[idnum][field]['present']
#                    print profile[idnum][field]['alphanumeric']
#                    print profile[idnum][field]['status']
