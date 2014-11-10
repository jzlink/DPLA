#!/usr/bin/env python

def find(dotstring, dictionary):
    '''accepts a json format dot string (eg:
    sourceResource.collection.title) and some dictonary
    and makes an index out of it. 
    Returns the value of the field if found in the dict and False if not.
    '''
    #parse dot string on '.' 
    # returns a list of fields eg: [sourceResource, collection, titl]
    #these are treated as successive keys below
    indexList = dotstring.split('.')

    #initialize a temporary container to the CHO record. It will change
    tempHolder = dictionary.copy()
    
    counter=0
    while counter < len(indexList):
        #if the tempHolder is a dict re-set the tempHolder to the
        # value of the next key in the indexList
        # if that key is not found return false
        if type(tempHolder) == dict:
            tempHolder = tempHolder.get(indexList[counter], False)
            
        #if the tempHolder is a list search each list item for the next
        # key in the indexList if it is found set tempHolder to the 
        # value found at that key
        # otherwise increment the 
        elif type(tempHolder) == list:
            notFoundCounter = 0
            for thing in tempHolder:
                if indexList[counter] in thing:
                    listIndex = tempHolder.index(thing)
                    tempHolder =\
                            tempHolder[listIndex][indexList[counter]]
                    found = True
                    break
                else:
                    notFoundCounter += 1
                        
            #if the end comes and the notFoundCounter is the size of the 
            # searched list (the field wasnt found in and list element)
            # set tempHolder to False
            if notFoundCounter == len(tempHolder):
                tempHolder = False
        # if the tempHolder is not a dict or list before the counter runs
        # out set it to false
        else:
            tempHolder = False

        #if at any point above the tempHolder has returned False
        # automatically push the counter to its limit 
        # (break the while loop)
        if tempHolder == False:
            counter = len(indexList)
            
        counter += 1
    return tempHolder


def test():
    DICT = {u'_id': u'digitalnc--urn:brevard.lib.unc.eduecu_c5:oai:digital.lib.ecu.edu/6570', u'admin': {u'sourceResource': {u'title': u'Bicycle'}, u'validation_message': None, u'valid_after_enrich': True}, u'sourceResource': {u'isPartOf': [u'https://digital.lib.ecu.edu/encore/ncgre000/00000007/00006570/00006570_tn_0001.gif'], u'description': [u'Two children standing behind a bicycle. Date from negative sleeve.'], u'language': [{u'iso639_3': u'eng', u'name': u'English'}], u'rights': u'Copyright held by Joyner Library. Permission to reuse this work is granted for all non-commercial purposes.', u'@id': u'http://dp.la/api/items/0625e0e117af61310a97a4366bbfa2d9#sourceResource', u'format': u'negatives (photographic)', u'contributor': [u'Daily Reflector (Greenville, N.C.)'], u'collection': {u'title': u'The Daily Reflector Image Collection', u'@id': u'http://dp.la/api/collections/3cbf478cc2d9d448daa7c73a42c3b0f2', u'id': u'3cbf478cc2d9d448daa7c73a42c3b0f2', u'description': u''}, u'date': {u'begin': u'1963-10-27', u'end': u'1963-10-27', u'displayDate': u'19631027'}, u'spatial': [{u'name': u'United States--North Carolina--Pitt County (N.C.)--Greenville (N.C.)'}], u'stateLocatedIn': [{u'name': u'North Carolina'}], u'title': [u'Bicycle'], u'identifier': u'https://digital.lib.ecu.edu/6570', u'type': u'image', u'subject': [{u'name': u'Children--North Carolina--Greenville'}, {u'name': u'Bicycles--North Carolina--Greenville'}, {u'name': u'Economics'}]}, u'_rev': u'1-7f9c2778b5f54282ef774863584fcf1d', u'object': u'https://digital.lib.ecu.edu/encore/ncgre000/00000007/00006570/00006570_tn_0001.gif', u'aggregatedCHO': u'#sourceResource', u'ingestDate': u'2014-09-29T22:53:53.010307Z', u'id': u'0625e0e117af61310a97a4366bbfa2d9', u'originalRecord': {u'about': {u'oaiProvenance:provenance': {u'xmlns:xsi': u'http://www.w3.org/2001/XMLSchema-instance', u'xsi:schemaLocation': u'http://www.openarchives.org/OAI/2.0/provenance http://www.openarchives.org/OAI/2.0/provenance.xsd', u'oaiProvenance:originDescription': {u'harvestDate': u'2014-09-18', u'oaiProvenance:metadataNamespace': u'http://www.openarchives.org/OAI/2.0/', u'oaiProvenance:baseURL': u'https://digital.lib.ecu.edu/oai/oai.aspx', u'oaiProvenance:datestamp': u'2014-09-18', u'altered': u'true', u'oaiProvenance:identifier': u'oai:digital.lib.ecu.edu/6570'}, u'xmlns:oaiProvenance': u'http://www.openarchives.org/OAI/2.0/provenance'}}, u'collection': {u'title': u'The Daily Reflector Image Collection', u'@id': u'http://dp.la/api/collections/3cbf478cc2d9d448daa7c73a42c3b0f2', u'id': u'3cbf478cc2d9d448daa7c73a42c3b0f2', u'description': u''}, u'header': {u'datestamp': u'2014-09-18', u'identifier': u'urn:brevard.lib.unc.eduecu_c5:oai:digital.lib.ecu.edu/6570', u'setSpec': u'ecu_c5'}, u'provider': {u'@id': u'http://dp.la/api/contributor/digitalnc', u'name': u'North Carolina Digital Heritage Center'}, u'id': u'urn:brevard.lib.unc.eduecu_c5:oai:digital.lib.ecu.edu/6570', u'metadata': {u'mods': {u'physicalDescription': {u'form': u'negatives (photographic)'}, u'xmlns': u'http://www.loc.gov/mods/v3', u'name': {u'namePart': u'Daily Reflector (Greenville, N.C.)', u'role': {u'roleTerm': u'contributor'}}, u'language': {u'languageTerm': u'eng'}, u'titleInfo': {u'title': u'Bicycle'}, u'identifier': u'https://digital.lib.ecu.edu/6570', u'relatedItem': {u'location': {u'url': u'https://digital.lib.ecu.edu/encore/ncgre000/00000007/00006570/00006570_tn_0001.gif'}}, u'note': [{u'#text': u'Two children standing behind a bicycle. Date from negative sleeve.', u'type': u'content'}, {u'#text': u'East Carolina University', u'type': u'ownership'}], u'accessCondition': u'Copyright held by Joyner Library. Permission to reuse this work is granted for all non-commercial purposes.', u'version': u'3.4', u'originInfo': {u'dateCreated': {u'#text': u'19631027', u'keyDate': u'yes'}}, u'location': [{u'url': {u'usage': u'primary display', u'access': u'object in context', u'#text': u'https://digital.lib.ecu.edu/6570'}}, {u'url': {u'access': u'preview', u'#text': u'https://digital.lib.ecu.edu/encore/ncgre000/00000007/00006570/00006570_tn_0001.gif'}}], u'xmlns:oai_dc': u'http://www.openarchives.org/OAI/2.0/oai_dc/', u'genre': u'still image', u'xmlns:xsi': u'http://www.w3.org/2001/XMLSchema-instance', u'xmlns:dc': u'http://purl.org/dc/elements/1.1/', u'xsi:schemaLocation': u'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd', u'subject': [{u'geographic': u'United States--North Carolina--Pitt County (N.C.)--Greenville (N.C.)'}, {u'topic': u'Children--North Carolina--Greenville'}, {u'topic': u'Bicycles--North Carolina--Greenville'}, {u'topic': u'Economics'}]}}}, u'score': 10.024311, u'ingestionSequence': 16, u'isShownAt': u'https://digital.lib.ecu.edu/6570', u'provider': {u'@id': u'http://dp.la/api/contributor/digitalnc', u'name': u'North Carolina Digital Heritage Center'}, u'@context': u'http://dp.la/api/items/context', u'ingestType': u'item', u'dataProvider': u'East Carolina University', u'@id': u'http://dp.la/api/items/0625e0e117af61310a97a4366bbfa2d9', u'@type': u'ore:Aggregation'}

    dotString = 'sourceResource.collection.description'
    value = find(dotString, DICT)

    print value

if __name__ == '__main__':
    test()
