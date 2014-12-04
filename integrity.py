#!/usr/bin/env python

import string


class Integrity():
    '''presides over a collection of methods that will validate lists, 
    dictionaries, or string/unicode items. Valid means containing at
    least one alphanumeric character. Currently accepted alphanumeric
    characters are all english characters a-z, capitol letters A-Z and
    digits 0-9. Special characters, characters with accent marks, and
    non-english characters are not recognized as valid.
    '''

    def __init__(self):
        #Sets stringvals to hold the set of acceptable valid characters
        self.stringVals = set(string.letters + string.digits)

    def validate(self, mystery_item):
        '''accepts a mystery item (string, list or dict)
        returns true if:
        a string/unicode as at least one alphanumeric character in it,
        OR a list has at least one element that has at least one
        alphanumberic character in it,
        OR a dictionary has at least one key/value pair where both key
        and value have at least one alphanumeric character it in
        else returns false
        '''
        valid = False
        item_type = type(mystery_item)

        if item_type == unicode or item_type == str:
            valid = self.validate_unicode(mystery_item)
        if item_type == list:
            valid = self.validate_list(mystery_item)
        if item_type == dict:
            valid = self.validate_dict(mystery_item)
        if item_type == int:
            self.validate_unicode(str(mystery_item))

        return valid
        
    def validate_unicode(self, item):
        '''accept a string or unicode item
        return true if there is a character in the item that matches
        the valid string. else return false
        ''' 
        valid = False
        #Find the set of characters that appear in item and stringVals,
        # if there is any return true.
        if len(set(item) & self.stringVals) > 0:
            valid = True

        return valid

    def validate_list(self, item):
        ''' accepts a list of anything
        returns true if one item in the list is valid
        '''
        valid = False

        #Counter to hold number of things in list that are valid
        valid_items = 0

        #Check if there are any items in the list
        if len(item) > 0:

            #Send each item to main validate method
            for element in item:
                valid_item = self.validate(element)

                #Count valid items
                if valid_item:
                    valid_items =+1

        if valid_items >0:
            valid = True

        return valid

    def validate_dict(self, item):
        '''accepts a dictionary
        returns true if there is at least one key/value pair such that
        the key is a vlaid string and the vlaue is vlaid anything else
        '''
        valid = False

        #Counter to hold number of things in dict that are valid
        valid_items = 0

        #Make sure there are items in the dict
        if len(item) > 0:

            #For each thing vlaidate the key
            for key in item:
                valid_key = self.validate(key)

                #If the key is valid send the value to the main method
                if valid_key:
                    valid_value = self.validate(item[key])

                    #Increment valid value counter
                    if valid_value:
                        valid_items =+ 1

        if valid_items > 0:
            valid = True
        return valid
                

def test():
    sr_dict = {u'isPartOf': [u'https://digital.lib.ecu.edu/encore/ncgre000/00000007/00006965/00006965_tn_0001.gif'], u'description': [u'Broken bicycle lying in the grass. Date from negative sleeve.'], u'language': [{u'iso639_3': u'eng', u'name': u'English'}], u'rights': u'Copyright held by Joyner Library. Permission to reuse this work is granted for all non-commercial purposes.', u'@id': u'http://dp.la/api/items/20f55d04eb9bc8c98b05151cd8cadbe3#sourceResource', u'format': u'negatives (photographic)', u'contributor': [u'Daily Reflector (Greenville, N.C.)'], u'collection': {u'title': u'The Daily Reflector Image Collection', u'@id': u'http://dp.la/api/collections/3cbf478cc2d9d448daa7c73a42c3b0f2', u'id': u'3cbf478cc2d9d448daa7c73a42c3b0f2', u'description': u''}, u'date': {u'begin': u'1964-03-14', u'end': u'1964-03-14', u'displayDate': u'19640314'}, u'spatial': [{u'name': u'United States--North Carolina--Pitt County (N.C.)--Greenville (N.C.)'}], u'stateLocatedIn': [{u'name': u'North Carolina'}], u'title': [u'Bicycle'], u'identifier': u'https://digital.lib.ecu.edu/6965', u'type': u'image', u'subject': [{u'name': u'Cycling accidents--North Carolina--Greenville'}, {u'name': u'Bicycles--North Carolina--Greenville'}, {u'name': u'Social and Family Life'}]}
    
    test_stringA = 'Some string'
    test_stringB = '@#$%^'
    test_stringC = ''

    test_unicodeA = u'Some unicode'
    test_unicodeB = u'%^&*('
    test_unicodeC = u' '

    test_listA = ['a', 'v', 'q', 'f']
    test_listB = ['@', '$', '']
    test_listC = ['', u'a', 'b', '']
    test_listD = ['']
    test_listE = []
    test_listF = [test_listA, test_listB]
    test_listG = [test_listB, test_listD]
    test_listH = [test_listB, test_stringA]

    test_dictA = {}
    test_dictB = {u'a':u'a thing', 'b':'b thing'}
    test_dictC = {'':''}
    test_dictD = {'':'', '':'a thing', 'a':''}
    test_dictE = {'a':'', '': 'c thing', 'b': 'b thing'}

    test_listI = [test_listB, test_unicodeB, test_dictA]
    test_listJ = [test_listB, test_unicodeB, test_dictB]    

    test_dictF = {'test_listA': test_listA}
    test_dictG = {'test_listE': test_listE}
    test_dictH = {'test_dictG': test_dictG, 'test_dictB': test_dictB}
    test_dictI = {'test_listA': test_listA, 'test_dictB': test_dictB, 
                  'test_unicodeA': test_unicodeA}
    test_dictJ = {'test_dictA': test_dictA, 'test_listB': test_listB,
                  'test_stringB': test_stringB}

    test_intA = 1

    test_item = test_intA

    test = IsAlphaNum()
    valid = test.validate(test_intA)

    print '%s is of type %s and is %s' % (test_item, type(test_item), valid)

if __name__ == '__main__':
    test()


