# -*- coding: utf-8 -*- 
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import json
def parse(file):
    fout = open('general.txt','w')
    data = {}
    for event, elem in ET.iterparse(file,events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                k = tag.attrib['k'].encode('utf-8')
                v = tag.attrib['v'].encode('utf-8')
                if not k in data:
                    data[k] = set([v])
                else:
                    data[k].add(v)
    return data
      
data = parse('sample.osm')
fout = open('general.txt','w')
for k in data:
    fout.write(k+':\n')
    for v in data[k]:
        fout.write(v+'|  ')
    fout.write('\n\n')
fout.write('\n\nkeys:\n')
for k in data:
    fout.write(k+'\n')
#pprint.pprint(data.keys())
 