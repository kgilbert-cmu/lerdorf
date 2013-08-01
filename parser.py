#!/usr/bin/env python

__author__  = "Kevin Gilbert"
__email__   = "kgilbert@andrew"

import xml.etree.ElementTree as ET
from optparse import OptionParser

# XML object tags, used to ensure we're looking at the right class of object
xml_doc = '{http://wherein.yahooapis.com/v1/schema}document'
toponym = '{http://wherein.yahooapis.com/v1/schema}placeDetails'

def is_toponym(object):
    return object.tag == toponym

'''
A toponym returned by the Yahoo API is an XML object of the "placeDetails"
class, and its location and geo-coordinates are stored in seperate fields
of the XML object. This function, reformat : ElementTree -> string, takes the
object and converts it to an "answer key" format. Example is provided below.

This function makes liberal use of magic numbers. These array indices should
probably take us to the latitude, longitude, and place name fields. For this
program, I ASSUME they will work. If they do not, we will have to develop a
more sophisticated method of parsing XML.

Example placeDetails XML object:
    <placeDetails>
      <placeId>1</placeId>
      <place>
        <woeId>2459115</woeId>
        <type>Town</type>
        <name><![CDATA[New York, NY, US]]></name>
        <centroid>
          <latitude>40.7146</latitude>
          <longitude>-74.0071</longitude>
        </centroid>
      </place>
      <placeReferenceIds>4</placeReferenceIds>
      <matchType>0</matchType>
      <weight>1</weight>
      <confidence>10</confidence>
    </placeDetails>

Example "answer key" result after reformat:
    "New York, NY, US[40.7146, -74.0071]"

'''
def reformat(placeDetails):
    # magic numbers ahoy!
    (lat,long) = (placeDetails[1][3][0].text, placeDetails[1][3][1].text)
    place_str = placeDetails[1][2].text
    return place_str + '['+lat+','+long+']'

def send(text, where, mode):
    if where == "":
        print text
    else:
        with open(where, mode) as output:
            output.write(text+'\n')

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="f", type="string",
                  help="incoming data on stdin", default="input.xml")
    parser.add_option("-o", "--where", dest="where", type="string",
                  help="outgoing data on stdout", default="")
    parser.add_option("-m", "--mode", dest="mode", type="string",
                  help="if mode == a then output is appended to previous text,\
                  else output overwrites previous text", default="w")
    (options, args) = parser.parse_args() # user input is stored in "options"

    tree = ET.parse(options.f)
    root = tree.getroot()

    if root[3].tag == xml_doc: # the only time that I check my magic number
        subtree = root[3]
        for XML in subtree:
            if is_toponym(XML):
                send(reformat(XML), options.where, options.mode)

if __name__ == "__main__":
    main()
