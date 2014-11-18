#!/usr/bin/env python

import yaml
import pprint
import collections #use collections.counter(list) for aggregating/counting
import string
import copy

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
#        self.DPLAData = dpla_fetch(api_key, 1, q= 'bicycle')
        self.isAlphaNum = IsAlphaNum()

    def createProfile(self):
        '''responsible for calling helper classes/methods and aggregating
        results. Returns a dictionary of CHO id's and their statuses
        '''
        #initialize dict to hold each document in a collection, 
        # its field's statuses and grade  
        collection = {}

        for CHO in self.DPLAData:
            itemMetadata= self.findVerify(CHO)

            collection.update(itemMetadata)


        return collection

    def findVerify(self, CHO):
        itemMeta = {}
        ID = CHO['id']
        fieldMetadata =  yaml.load(open('fields.yml', 'r'))
        for field in fieldMetadata:
            #call the finder method
            fieldValue = find(field,CHO)

            if fieldValue == False:
                fieldMetadata[field]['present'] = False

            else:
                fieldMetadata[field]['present'] = True
                if len(fieldValue) > 0:
                    fieldMetadata[field]['empty'] = False
                    alphaNum = self.isAlphaNum.validate(fieldValue)
                    if alphaNum:
                        fieldMetadata[field]['alphanumeric'] = True
                    else:
                        fieldMetadata[field]['alphanumeric'] = False
                        
                else:
                    fieldMetadata[field]['empty'] = True                    
                    
        itemMeta[ID] = fieldMetadata

        return itemMeta

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
    for item in profile:
        print item
        for field in profile[item]:
            print '%s: Alphanumeric %s' %(field, profile[item][field]['alphanumeric'])
#    pprint.pprint(test.DPLAData)
#    pprint.pprint(profile)




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
