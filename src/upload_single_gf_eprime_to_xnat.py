#!/usr/bin/env python
#
# Given the name of an E-PRIME .txt output file, parse the filename and upload the file
# to the appropriate EPRIME_TXT resource on XNAT. Specific to the three GF tasks.
#
# Requires a python 3 installation and DAX:
#    https://dax.readthedocs.io/en/latest/installing_dax_in_a_virtual_environment.html
#
#
# How filenames are parsed - bits marked with ^ are extracted.
# 
#    Filename as saved by E-PRIME:   Oddball-123456-1-run 1.txt
#                                    ^       ^      ^
#    Matching session on XNAT:       123456
#    Matching scan label on XNAT:    oddball1*
#
#
#    Filename as saved by E-PRIME:   SPT-123456-1.txt
#                                    ^   ^      ^
#    Matching session on XNAT:       123456
#    Matching scan label on XNAT:    spt1*
#
#
#    Filename as saved by E-PRIME:   WM-123456-2-run3.txt
#                                    ^  ^      ^
#    Matching session on XNAT:       123456
#    Matching scan label on XNAT:    wm2*
#
#
# In some scenarios nothing will be uploaded and a warning will be shown. These situations
# can be handled manually:
#    - A matching scan isn't found on XNAT
#    - More than one matching scan is found on XNAT
#    - One matching scan is found on XNAT, but it already has an EPRIME_TXT resource and
#          the --overwrite option was not specified


import re
import os
import dax
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Upload an E-Prime .txt to XNAT')
parser.add_argument('--eprime_txt', help='E-Prime .txt filename',required=True)
parser.add_argument('--project', help='XNAT project',required=True)
parser.add_argument('--overwrite', help='Force overwrite if existing',default='False')
args = parser.parse_args()

expr = re.compile('^(?P<task>.*?)-(?P<session>.*?)-(?P<run>\d).*\.txt$')

project = args.project
overwrite = args.overwrite
eprime_txt = args.eprime_txt

r = expr.match(os.path.basename(eprime_txt))

session = r.group('session')
subject = r.group('session')
run = r.group('run')
task = r.group('task')

print('Project: %s' % project)
print('Session: %s' % session)
print('Subject: %s' % subject)
print('Run:     %s' % run)
print('Task:    %s' % task)

# Find the usable scan with appropriate label and verify there's only one
#
# wm1*
# wm2*
# oddball1*
# oddball2*
# spt1*
scan_prefix = '%s%s' % (task.lower(),run)


with dax.XnatUtils.get_interface() as xnat:
    
    # List of scans
    scans = xnat.get_scans(project,session,subject)

    # Find scan(s) where scan_prefix matches scans['scan_label']
    match = [x for x in scans if x['scan_type'].startswith(scan_prefix)]
    
    # If length of matches isn't 1 warn and skip upload
    if len(match) != 1:
        raise Exception('Wrong number of scans matched (%d)' % len(match))
    else:
        match = match[0]
        print('Found single scan %s matching \'%s\'' % (match['scan_id'],scan_prefix))
        
    # If scan has resource warn and skip upload unless overwrite
    rsrc = xnat.select_scan_resource(project,session,subject,match['scan_id'],'EPRIME_TXT')
    if rsrc.exists() and not (overwrite.lower()=='true'):
        print('WARNING: EPRIME_TXT resource exists, skipping')
    else:
        if not rsrc.exists():
            rsrc.create()
        rsrc.put([eprime_txt],overwrite=True)
        print('Uploaded %s' % eprime_txt)

