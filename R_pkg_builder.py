'''This script points to an R library directory and an
output directory, and--provided a zip executable--creates
an R packages repositiory in the output directory'''

import os, sys
from subprocess import call, check_output
from rpy2.robjects.packages import importr

LIBFOLDER = os.getenv('LIBFOLDER', '/usr/lib/R/library')
OUTFOLDER = os.getenv('OUTFOLDER', os.getcwd())
ZEXEC = os.getenv('ZEXEC', '/usr/bin/zip')

def extract_version(file):
    '''Return version number from an R Description file.
       Example:
       extract_version('/usr/lib/R/library/base/DESCRIPTION')'''
    stream = open(file, 'r').read().replace('\t','').split('\n')
    d = {}
    for x in stream:
        try:
            k,v = x.split(':')
            d[k] = v
        except: pass
    version = d['Version'].strip()
    return version 

def zipit(libfolder, outfolder, exec):
    '''for each package in libfolder, extracts version number
       to use in naming a zip file. Zips package to outfolder
       in correct format.'''
    old_wd = os.getcwd()
    os.chdir(libfolder)
    for dir in os.listdir():
        try:
            v = extract_version(dir+'/DESCRIPTION')
            call([exec, '-r', outfolder+'/'+dir+'_'+v+'.zip',
                  dir])
        except:
            pass
    os.chdir(old_wd)

def create_PACKAGES(outfolder):
    '''Call R tools::write_PACKAGES function to create
       PACKAGES file needed for repo'''
    rtools = importr('tools')
    rtools.write_PACKAGES(outfolder, type='win.bin')

def main(libfolder=LIBFOLDER, outfolder=OUTFOLDER, exec=ZEXEC):
    '''Loops through directories in libfolder, zips them, names
       zip files based on version number, and builds the PACKAGES file'''
    zipit(libfolder, outfolder, exec)
    create_PACKAGES(outfolder)
    
if __name__ == '__main__':
    sys.exit(main())
