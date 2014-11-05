#!/usr/bin/env python

def validate(self, sortedDict):
    ''' accepts dics of items with lists of their sorted fields
    matches a full CHO record in DPLAData to each item, validates data
    returns an updated sorted dict reflecting validity checks'''

    validator = Validator()
    emptyField = []
    
    #for each item in the sorted dict match item to full CHO record
    # from DPLA
    for item in sortedDict:
        for CHO in self.DPLAData:
            if CHO['id'] == item:
                record = CHO
             
        if item != 'fails':
            for fieldList in sortedDict[item]:
                if 'missing' not in fieldList:
                    for field in sortedDict[item][fieldList]:
                        if 'collection.' not in field:
                            if fieldList == 'required_general':
                                index = record[field]
                            else:
                                index = record['sourceResource'][field]
