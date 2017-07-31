#!/usr/bin/env python
'''
Takes a PREMIS CSV file, as generated by premiscsv.py, and transform into XML.
'''
import sys
import csv
from lxml import etree

def extract_metadata(csv_file):
    '''
    Read the PREMIS csv and store the metadata in a list of dictionaries.
    '''
    object_dictionaries = []
    input_file = csv.DictReader(open(csv_file))
    for rows in input_file:
        object_dictionaries.append(rows)
    return object_dictionaries

def add_value(value, element):
    '''
    Useless helper function - remove!
    '''
    element.text = value


def write_premis(doc, premisxml):
    '''
    Writes the PREMIS object to a file.
    '''
    with open(premisxml, 'w') as out_file:
        doc.write(out_file, pretty_print=True)


def create_unit(index, parent, unitname):
    '''
    Helper function that adds an XML element.
    '''
    premis_namespace = "http://www.loc.gov/premis/v3"
    unitname = etree.Element("{%s}%s" % (premis_namespace, unitname))
    parent.insert(index, unitname)
    return unitname

def setup_xml(object_dictionaries):
    '''
    This should just create the PREMIS lxml object.
    Actual metadata generation should be moved to other functions.
    '''
    namespace = '<premis:premis xmlns:premis="http://www.loc.gov/premis/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/premis/v3 https://www.loc.gov/standards/premis/premis.xsd" version="3.0"></premis:premis>'
    premis_namespace = "http://www.loc.gov/premis/v3"
    xsi_namespace = "http://www.w3.org/2001/XMLSchema-instance"
    premis = etree.fromstring(namespace)
    doc = etree.ElementTree(premis)
    for objects in object_dictionaries:
        id_list = objects['objectIdentifier'].replace(
            '[', ''
        ).replace(']', '').replace('\'', '').split(', ')
        object_parent = create_unit(
            0, premis, 'object'
        )
        object_parent.attrib[
            "{%s}type" % xsi_namespace
        ] = "premis:%s" % objects['objectCategory']
        object_identifier_uuid = create_unit(
            2, object_parent, 'objectIdentifier'
        )
        object_identifier_uuid_type = create_unit(
            1, object_identifier_uuid, 'objectIdentifierType'
        )
        object_identifier_uuid_value = create_unit(
            2, object_identifier_uuid, 'objectIdentifierValue'
        )
        add_value(id_list[0], object_identifier_uuid_type)
        add_value(id_list[1], object_identifier_uuid_value)
        if objects['objectCategory'] == 'file':
            object_characteristics = create_unit(
                10, object_parent, 'objectCharacteristics'
            )
            fixity = create_unit(
                0, object_characteristics, 'fixity'
            )
            size = create_unit(
                1, object_characteristics, 'size'
            )
            size.text = objects['size']
            message_digest_algorithm = create_unit(
                0, fixity, 'messageDigestAlgorithm'
            )
            message_digest = create_unit(
                1, fixity, 'messageDigest'
            )
            message_digest_originator = create_unit(
                2, fixity, 'messageDigestOriginator'
            )
            message_digest_originator.text = objects['messageDigestOriginator']
            message_digest.text = objects['messageDigest']
            message_digest_algorithm.text = objects['messageDigestAlgorithm']
    print(etree.tostring(doc, pretty_print=True))
    return premis_namespace, doc, premis
def main():
    '''
    Launches all the other functions when run from the command line.
    For debugging purposes, the contents of the CSV is printed to screen.
    '''
    csv_file = sys.argv[1]
    object_dictionaries = extract_metadata(csv_file)
    setup_xml(object_dictionaries)
    '''
    for x in object_dictionaries:
        for i in x:
            if x[i] != '':
                print i, x[i]
        print '\n'
    '''
if __name__ == '__main__':
    main()
