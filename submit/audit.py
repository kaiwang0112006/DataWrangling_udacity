# -*- coding: utf-8 -*- 
"""
- Audits the OSMFILE and changes the variable 'mapping' to reflect the changes
    needed to fix the unexpected street types to the appropriate ones in the
    expected list. Mappings have been added only for the actual problems found
    in this OSMFILE, not for a generalized solution, since that may and will
    depend on the particular area being audited.
- The update function fixes the street name. It takes a string with a street
    name as an argument and returns the fixed name.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample.osm"

street_type_re = re.compile(r'\bSt\.?$', re.IGNORECASE)

mapping = { "St": "Street",
            "ave.": "Avenue",
            "Rd": "Road",
            "St.": "Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def correct_street_type(street_name):
    changed = 0
    street_name = street_name.strip()
    words = street_name.split()
    newwords = ''
    # change street abbreviation to full name
    for w in words:
        if w in mapping:
            newwords += mapping[w] + ' '
        else:
            newwords += w + ' '
    if street_name != newwords[:-1]:
        #print street_name + '=>' + newwords[:-1]
        changed = 1

    return newwords[:-1], changed

def correct_postcode(postcode):
    changed = 0
    if "-" in postcode:
        return None,1
    else:
        return postcode,0
    
def correct_number(num):
    changed = 0
    newnum = ''
    if " / " in num:
        newnum = foreachnum(num," / ")
    elif ';' in num:
        newnum = foreachnum(num,";")
    elif "+8610-88087384" in num and "88086667" in num: #"+8610-88087384；88086667" which contain a unicode ';'
        ewnum = foreachnum('+8610-88087384;88086667',";")
    elif len(num.split('/')[0]) == (len(num)-1)/2:
        newnum = foreachnum(num,"/")
    else:
        newnum = purenum(num)

    #print num + '=>' + newnum
    if num == newnum:
        return num, 0
    else:
        return newnum, 1

def foreachnum(allnum,seq):
    r = ''
    for n in allnum.split(seq):
        n = purenum(n)
        r = r + n +','
    r = r[:-1] 
    return r

def purenum(num):
    r = ''
    for i in num:
        try:
            int(i)
            r += i
        except:
            pass
    if r[:4] == "8610":
        r = "86010"+r[4:]
    elif r[:5] == "86010":
        r = "86010"+r[5:]
    elif r[:2] == '00':
        r = r[2:]
        
    return r

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    audited = {'Overabbreviated':[],"wrongpostcode":[],"wrongnumber":[]}
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    v, c = correct_street_type(tag.attrib['v'])
                    if c:
                        audited['Overabbreviated'].append((tag.attrib['v'], v))
                elif tag.attrib['k'] == "addr:postcode":
                    v, c = correct_postcode(tag.attrib['v'])
                    if c:
                        audited['wrongpostcode'].append((tag.attrib['v'], v))
                elif tag.attrib['k'] == "fax" or tag.attrib['k'] == "phone":
                    v, c = correct_number(tag.attrib['v'])
                    if c:
                        audited['wrongnumber'].append((tag.attrib['v'], v))

    osm_file.close()
    return audited


def test():
    audited = audit(OSMFILE)
    pprint.pprint(audited)


if __name__ == '__main__':
    test()