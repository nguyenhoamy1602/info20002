# Nguyen Hoa My
# 836385
# Wednesday 9-11am

import csv
from collections import defaultdict as dd
from math import floor


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


def properties(ordered_data):
    # helper function take in an ordered list
    # return a dictionary of 5 number summary

    # find the length of data, median rank and quartile rank
    n = float(len(ordered_data))
    median_rank = (n+1)/2
    median_index = int(floor(median_rank))
    q1_rank = float(median_index+1)/2
    q3_rank = median_index + q1_rank

    # create a dictionary
    num_sum = dd(float)

    num_sum['median'] = median(ordered_data, median_rank)
    num_sum['q1'] = median(ordered_data, q1_rank)
    num_sum['q3'] = median(ordered_data, q3_rank)
    num_sum['min'] = min(ordered_data)
    num_sum['max'] = max(ordered_data)

    return num_sum


def modes(data):
    # helper function take in a list and return modes
    # create dictionary
    dic_data = dd(int)
    for i in data:
        dic_data[i] += 1
    modelist = []
    maxfreq = 0

    # iterate through value of dictionary to determine modes
    for item in dic_data:

        # item with higher frequency creates a new modelist
        if dic_data[item] > maxfreq:
            modelist = [item]
            maxfreq = dic_data[item]

        # item with same frequency is added
        elif dic_data[item] == maxfreq:
            modelist.append(item)

    return sorted(modelist)


# open CSV file and read it
csvFile = open('input.csv')
csvData = csv.reader(csvFile)

# create XML file and write into it
xmlFile = 'output.xml'
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0"?>' + '\n')

# include DTD
xmlData.write('<!DOCTYPE attributes [' + '\n')
xmlData.write('  <!ELEMENT attributes (attribute*)>' + '\n')
xmlData.write('  <!ELEMENT attribute (name, properties?, modes?, uniques?)>' +
              '\n')
xmlData.write('  <!ELEMENT name (#PCDATA)>'+'\n')
xmlData.write('  <!ELEMENT properties (property+)>'+'\n')
xmlData.write('  <!ELEMENT property (#PCDATA)>'+'\n')
xmlData.write('  <!ELEMENT modes (mode+)>'+'\n')
xmlData.write('  <!ELEMENT mode (#PCDATA)>'+'\n')
xmlData.write('  <!ELEMENT uniques (unique+)>'+'\n')
xmlData.write('  <!ELEMENT unique (#PCDATA)>'+'\n')
xmlData.write('  <!ATTLIST attribute type (integer|float|string) #REQUIRED>' +
              '\n')
xmlData.write('  <!ATTLIST property name (min|q1|median|q3|max) #REQUIRED>' +
              '\n')
xmlData.write(']>'+'\n')

xmlData.write('<attributes>' + '\n')

# get columns of data
columns = dd(list)
for row in csvData:
    for (i, v) in enumerate(row):
        columns[i].append(v)

# iterate through columns to write data into XML file
for i in range(len(columns)):

    # determine attribute type
    data = columns[i][1:]
    att_type = data_type(data)
    xmlData.write('  ' + '<attribute type = "' + att_type + '">' '\n')
    xmlData.write('     ' + '<name>' + '<![CDATA[' + columns[i][0] +
                  ']]>' + '</name>' + '\n')


    # if data is integer or float, find 5 number summary
    if att_type != 'string':
        xmlData.write('     ' + '<properties>' + '\n')

        ordered_data = sorted([float(num) for num in data])
        num_list = ['min', 'q1', 'median', 'q3', 'max']
        num_sum = properties(ordered_data)
        for value in num_list:
            if att_type == 'integer':
                if num_sum[value].is_integer():
                    num_sum[value] = int(num_sum[value])
            xmlData.write('       ' + '<property name = "' + i + '">' +
                          str(num_sum[i]) + '</property>' + '\n')
        xmlData.write('     ' + '</properties>' + '\n')

    # find modes
    xmlData.write('     ' + '<modes>' + '\n')

    modelist = modes(data)
    for mode in modelist:
        xmlData.write('         ' + '<mode> ' + '<![CDATA[' + mode + ']]>' +
                      ' </mode>' + '\n')
    xmlData.write('     ' + '</modes>' + '\n')

    # if data is string, find unique values
    if att_type == 'string':
        xmlData.write('     ' + '<uniques>' + '\n')

        # use set
        uniques = set(sorted([string for string in data]))

        for value in uniques:
            xmlData.write('         ' + '<unique>' + '<![CDATA[' +
                          str(value) + ']]>' + '</unique>' + '\n')
        xmlData.write('     ' + '</uniques>' + '\n')

    xmlData.write('  ' + '</attribute>' + '\n')

xmlData.write('</attributes>' + '\n')

# close XML and CSV file
xmlData.close()
csvFile.close()
