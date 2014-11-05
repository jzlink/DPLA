#!/usr/bin/env python

import yaml
import pprint

from dpla_utils import * 

class Sorter():
    '''Responsible for sorting fields in data receieve by the DPLA into
    present/missing and required/recommended fields
    '''
    def __init__(self, dataDict):
        self.DPLAData = dataDict
        self.fields = yaml.load(open('fields.yml', 'r'))
        self.catagories = yaml.load(open('fieldCatagories.yml', 'r'))
        self.sortedFields = {}
        #count of records DPLA fails to provide its DPLA required fields for
        #Anticipating it will remain )
        self.fails = 0
        self.sortedFields['fails'] = self.fails
        
    def sort(self):
        '''Given a dict (assumed to be data from DPLA) sort fields according 
        to metadata. Return dict of items and lists of their sorted fields 
        also includes number of records the DPLA failed to provide its core 
        data on as fails. example return value:
        {item_id: {required_SR: [], required_general: [], recommended: [], 
        missing_SR:[], missing_general: [], missing_reccomended: [] 
        conditional: []} fails : 0}
        '''

        for CHO in self.DPLAData:

            compiled = {}

            #get keys present in data
            general_keys, SR_keys, DPLA_keys = self.getKeys(CHO)
            
            #sort keys into lists of fields based on metadata
            #loop through catagories established in metadata
            for catagory in self.catagories:
                #use metadata to decide which set of keys to analyse  
                keys_needed = self.catagories[catagory]['key_list']
                if keys_needed == 'SR':
                    keys = SR_keys
                else:
                    keys  = general_keys

                present_list, missing_list = \
                                            self.getFields(catagory, keys, CHO)
 
                #use metadata to properly name resulting lists
                present_name = self.catagories[catagory]['present_list']
                missing_name =self.catagories[catagory]['missing_list']

                compiled[present_name] = present_list
                compiled[missing_name] = missing_list

            #if the DPLA has not failed on this record, add it to dict
            if len(DPLA_keys) == len(self.fields['DPLA']):
                self.sortedFields[CHO['id']] = compiled

            else:
                self.fails = self.fails + 1
                self.sortedFields['fails'] = self.fails 

        return self.sortedFields
        
    def getKeys(self, CHO):
        '''given a single DPLA record, retrieve fields as keys from multiple
        levels of data hierarchy. return 3 lists of keys: 
        general, sourceResource and DPLA
        '''
        general_keys = []
        SR_keys = []
        DPLA_keys = []

        #get all keys present at the highest level of the data hierarchy
        for field in CHO:
            general_keys.append(field)
        
            #if field is a DPLA required field append DPLA.keys
            if field in self.fields['DPLA']:
                DPLA_keys.append(field)
                
        #get all keys present at the SR level of the data hierarchy
        for field in CHO['sourceResource']:
            SR_keys.append(field)

        return general_keys, SR_keys, DPLA_keys

    def getFields(self, catagory, keys, CHO):
        ''' Given a specific DPLA record, a field catagory, and a set of keys
        determine which fields in the catagory are present in the keys. Create 
        lists of present and missing fields accordingly. Return 2 lists:
        present and required.
        '''

        present_list = []
        missing_list = []
            
        #use two sets of yaml metadata to get proper list of fields for
        #  comparasin
        needed_field_list = self.catagories[catagory]['fields_list']
        field_list = self.fields[needed_field_list]


        #compare catagory field list to list of keys. Add to correct list
        for field in field_list:
            if field in keys:
                present_list.append(field)
            else:
                missing_list.append(field)
                
        #for the recommended catagory do the conditional checks
        if catagory == 'recommended':
            present_list, missing_list = \
                    self.conditionalCheck(present_list, missing_list, CHO)

        return present_list, missing_list


    def conditionalCheck(self, present_list, CHO):
        '''Some recommended fields only count as present if they have 
        fulfilled proper sub-fields. Given the CHO and the list of recommened
        fields preform checks on these fields specifically. Adjust present and
        missing lists if necessary and return
        '''
        present_subfields = []
        fields_missing_subfield = []
        for field in self.fields['conditional_subfields']:
            sub_field = self.fields['conditional_subfields'][field]

            if field in present_list:

                #collection field needs special handeling because it hads
                # two conditional fields that are both recommended (not
                # required) so there absence is noted but is not disqualifying
                if field == 'collection':
                    for s_field in sub_field:
                        if sub_field in CHO['sourceResource'][field]:

                        else:
                            missing_list.append(c_field)

                else:
                    #find out what type SR sub_field each thing is
                    #adjust CHO index accordingly                           
                    field_type = type(CHO['sourceResource'][field])
                    check_field = ''
                    if field_type == list:
                        check_field = CHO['sourceResource'][field][0]
                    else:
                        check_field = CHO['sourceResource'][field]

                    #put it all together and check for conditional field    
                    if sub_field not in check_field:
                        present_list.remove(field)
                        missing_list.append(field)

        return present_list, missing_list

def test():
    
    api_key = '2992771ce4f801b3c6ba94f38366c102'
    DPLAData = dpla_fetch(api_key, 20, q= 'bicycle')

    test = Sorter(DPLAData)
    oo_sort= test.sort()
    pprint.pprint(oo_sort)

 #   for CHO in test.DPLAData:
 #       g, sr, DPLA = test.getKeys(CHO)
 #       pprint.pprint(test.getFields('recommended', sr, CHO))
        

#    pprint.pprint(test.DPLAData)

if __name__ == '__main__':
    test()
