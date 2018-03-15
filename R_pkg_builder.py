'''This script points to an R library directory (LIBFOLDER) where built R
packages are (non-zipped) and--provided a zip executable (ZEXEC)--creates
an R package repositiory in the output directory (OUTFOLDER).

LIBFOLDER, OUTFOLDER, and ZEXEC can be passed as arguments:
python R_pkg_builder.py LIBFOLDER=/usr/lib/R/library OUTFOLDER=$(pwd) ZEXEC=$(which zip)

The zip files and the PACKAGES file this script creates in the output
directory can be used in R's install.packages() function, as in:
install.packages(repos='path to repo', type='win.bin')
'''

import os, sys
from subprocess import call, check_output
from rpy2.robjects.packages import importr

# Pull variables in from passed arguments:
if len(sys.argv) > 1:
    for arg in sys.argv[1:len(sys.argv)]:
        try:
            k,v = arg.split('=')
            exec(k.upper()+'='+"\'"+v+"\'")
        except:
            pass


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
    if LIBFOLDER not in globals():
        sys.exit('LIBFOLDER not set. Need to set LIBFOLDER, OUTFOLDER, and ZEXEC')
    if OUTFOLDER not in globals():
        sys.exit('OUTFOLDER not set. Need to set LIBFOLDER, OUTFOLDER, and ZEXEC')
    if ZEXEC not in globals():
        sys.exit('ZEXEC not set. Need to set LIBFOLDER, OUTFOLDER, and ZEXEC')
    sys.exit(main())
