#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then
clean it up. In the first exercise we want you to audit the datatypes that can be found in some 
particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a set of the datatypes
that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import sys

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]


def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    fin = csv.DictReader(open(filename))
    
    for eachline in fin:
        for fds in FIELDS:
            if not fieldtypes.has_key(fds):
                fieldtypes[fds] = []
            value = eachline[fds]
            if value == '' or value == 'NULL':
                if "NoneType" not in fieldtypes[fds]:
                    fieldtypes[fds].append(type(None))
            elif value[0] == "{":
                if "list" not in fieldtypes[fds]:
                    fieldtypes[fds].append(type([])) 
            elif "e+" in value:
                if "float" not in fieldtypes[fds]:
                    fieldtypes[fds].append(type(1.1))  
                
            else:
                try:
                    int(value)
                    if "int" not in fieldtypes[fds]:
                        fieldtypes[fds].append(type(1))                          
                except:
                    pass                 
                
                try:
                    if float(value) - int(float(value)) != 0.0:
                        if "float" not in fieldtypes[fds]:
                            fieldtypes[fds].append(type(1.1))                        
                except:
                    #print sys.exc_info()[0],sys.exc_info()[1]
                    pass
    for fds in fieldtypes:
        fieldtypes[fds] = set(fieldtypes[fds])
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
