# Nguyen Hoa My
# 836385
# Wednesday 9-11am

import csv
from collections import defaultdict as dd
from math import floor
from lxml import etree


def data_type(data):
    # helper function take in a list and return attribute type
    att_type = 'integer'

    for element in data:

        # test if the string is an integer
        if element.isdigit():
            att_type = 'integer'

        else:
            # test if the string is float
            try:
                float(element)
                att_type = 'float'
                return att_type

            except ValueError:
                att_type = 'string'
                return att_type
    return att_type


def median(data, rank):
    # helper function take in an ordered list and rank and return median

    if rank.is_integer():
        median = data[int(rank-1)]
    else:
        median = float(data[int(rank - 1.5)] + data[int(rank - 0.5)])/2

    return median


def properties_fn(ordered_data):
    # helper function take in an ordered list
    # return a dictionary of 5 number summary

    # find the length of data, median rank and quartile rank
    n = float(len(ordered_data))
    median_rank = (n+1)/2
    median_index = int(floor(median_rank))
    q1_rank = float(median_index+1)/2
    q3_rank = median_index + q1_rank

    # create a dictionary
    properties = dd(float)

    # update values in dictionary
    properties['median'] = median(ordered_data, median_rank)
    properties['q1'] = median(ordered_data, q1_rank)
    properties['q3'] = median(ordered_data, q3_rank)
    properties['min'] = min(ordered_data)
    properties['max'] = max(ordered_data)

    return properties


def modes(data):
    # helper function take in a list and return modes list

    # create dictionary
    dic_data = dd(int)

    # iterate through list to find items' frequency
    for i in data:
        dic_data[i] += 1
    modelist = []
    maxfreq = 0

    # iterate through items of dictionary to determine modes
    for item in dic_data:

        # item with higher frequency creates a new modelist
        if dic_data[item] > maxfreq:
            modelist = [item]
            maxfreq = dic_data[item]

        # item with same frequency is added
        elif dic_data[item] == maxfreq:
            modelist.append(item)

    return sorted(modelist)


# main function

# open CSV file and read it
csvFile = open('input.csv')
csvData = csv.reader(csvFile)

# create XML file and write into it
xmlFile = 'output.xml'
xmlData = open(xmlFile, 'w')

# get data in columns
columns = dd(list)
for row in csvData:
    for (i, v) in enumerate(row):
        columns[i].append(v.strip())

# set 'attributes' as root
root = etree.Element('attributes')

# iterate through each column
for i in range(len(columns)):
    data = columns[i][1:]

    # find attribute type
    att_type = data_type(data)

    # set 'attribute' as child
    child = etree.SubElement(root, 'attribute', type=att_type)

    # set 'name'
    child_name = etree.SubElement(child, 'name')
    child_name.text = etree.CDATA(columns[i][0])

    # find 5 number summary for float and integer
    if att_type != 'string':
        child_properties = etree.SubElement(child, 'properties')
        ordered_data = sorted([float(num) for num in data])
        property_list = ['min', 'q1', 'median', 'q3', 'max']
        properties = properties_fn(ordered_data)
        for value in property_list:
            if att_type == 'integer':
                if properties[value].is_integer():
                    properties[value] = int(properties[value])
            child_property = etree.SubElement(child_properties, 'property',
                                              name=value)
            child_property.text = str(properties[value])

    # find 'modes'
    child_modes = etree.SubElement(child, 'modes')
    modelist = modes(data)
    for mode in modelist:
        child_mode = etree.SubElement(child_modes, 'mode')
        child_mode.text = etree.CDATA(mode)

    # find uniques values for string
    if att_type == 'string':
        child_uniques = etree.SubElement(child, 'uniques')

        # use set
        uniques = sorted(set([string for string in data]))
        for value in uniques:
            child_unique = etree.SubElement(child_uniques, 'unique')
            child_unique.text = etree.CDATA(value)

# include DTD
doc = ('<!DOCTYPE attributes [' +
       '<!ELEMENT attributes (attribute*)>' +
       '<!ELEMENT attribute (name, properties?, modes?, uniques?)>' +
       '<!ELEMENT name (#PCDATA)>' +
       '<!ELEMENT properties (property+)>' +
       '<!ELEMENT property (#PCDATA)>' +
       '<!ELEMENT modes (mode+)>' +
       '<!ELEMENT mode (#PCDATA)>' +
       '<!ELEMENT uniques (unique+)>' +
       '<!ELEMENT unique (#PCDATA)>' +
       '<!ATTLIST attribute type (integer|float|string) #REQUIRED>' +
       '<!ATTLIST property name (min|q1|median|q3|max) #REQUIRED>' +
       ']>')

# create content
content = etree.tostring(root, pretty_print=True,
                         xml_declaration=True,
                         encoding='utf-8',
                         doctype=doc)
# write to XML file
xmlData.write(content)

# close XML and CSV file
xmlData.close()
csvFile.close()
