#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit import *


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    # you should process only 2 types of top level tags: "node" and "way"
    if element.tag == "node" or element.tag == "way" :
        for key in element.attrib.keys():
            val = element.attrib[key]
            node["type"] = element.tag
            
            # If key in CREATED list, store key-val under "created"
            if key in CREATED:
                if not "created" in node.keys():
                    node["created"] = {}
                node["created"][key] = val
                
            # Fetch coordinates 
            elif key == "lat" or key == "lon":
                if not "pos" in node.keys():
                    node["pos"] = [0.0, 0.0]
                old_pos = node["pos"]
                if key == "lat":
                    new_pos = [float(val), old_pos[1]]
                else:
                    new_pos = [old_pos[0], float(val)]
                node["pos"] = new_pos
            else:
                node[key] = val
                
             # Begin iterating over subtags
            for tag in element.iter("tag"):
                tag_key = tag.attrib['k']
                tag_val = tag.attrib['v']
                
                # Check for problem characters
                if problemchars.match(tag_key):
                    continue
                
                # fix tag 'v' attribute of streetname and postcode
                elif tag_key.startswith("addr:"):
                    if not "address" in node.keys():
                        node["address"] = {}
                    addr_key = tag.attrib['k'][len("addr:") : ]
                    if lower_colon.match(addr_key):
                        continue
                    else:
                        if tag.attrib['k'] == "addr:street":
                            fixed_v, change = correct_street_type(tag_val)
                        elif tag.attrib['k'] == "addr:postcode":
                            fixed_v, change = correct_postcode(tag.attrib['v'])
                        else:
                            fixed_v = tag_val
                        if fixed_v != None:
                            node["address"][addr_key] = fixed_v
                
                # fix fax and phone number
                elif tag_key == "fax" or tag_key == "phone":
                    fixed_v, chang = correct_number(tag_val)
                    node[tag_key] = fixed_v
                    
                #fix multiple tag_key confusing. These two tag_key in the list have same meaing, 
                #so just keep the latter one in the list and change the former to the latter
                elif tag_key in [ u'应急避难场所疏散人数万人',u'应急避难场所疏散人口万人']:
                    node[u'应急避难场所疏散人口万人'] = tag_val
                    
                # '疏散人数' and '疏散人数（万）' are two similar tag_key. Inthis way below, we change '疏散人数' to '疏散人数（万）'
                # by doing some math.
                elif tag_key == u'疏散人数':
                    node[u'疏散人数（万）'] = str(round(float(tag_val.split()[0].replace(',',''))/10000,2))
                elif tag_val != None:
                    node[tag_key] = tag_val
        for tag in element.iter("nd"):
            if not "node_refs" in node.keys():
                node["node_refs"] = []
            node_refs = node["node_refs"]
            node_refs.append(tag.attrib["ref"])
            node["node_refs"] = node_refs

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('sample.osm', False)
    #pprint.pprint(data[:2])


if __name__ == "__main__":
    test()