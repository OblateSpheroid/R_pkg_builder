import os, sys
import yaml
from subprocess import call, check_output
from rpy2.robjects.packages import importr

LIBFOLDER = os.getenv('LIBFOLDER', '/usr/lib/R/library')
OUTFOLDER = os.getenv('OUTFOLDER', os.getcwd())
ZEXEC = os.getenv('ZEXEC', '/usr/bin/tar')

def extract_version(file):
    '''Return version number from an R Description file.
       Example:
       extract_version('/usr/lib/R/library/base/DESCRIPTION')'''
    stream = open(file, 'r').read().replace('\t','')
    y = yaml.load(stream)
    return y['Version']

def zipit(libfolder, outfolder, exec):
    '''for each package in libfolder, extracts version number
       to use in naming a zip file. Zips package to outfolder
       in correct format.'''
    old_wd = os.getcwd()
    os.chdir(libfolder)
    for dir in os.listdir(libfolder):
        try:
            v = extract_version(dir+'/DESCRIPTION')
            call([exec,<zip command>,dir,
                  outfolder+'/'+dir+'_'+v+'.zip'])
        except:
            pass
    os.chdir(old_wd)

def create_PACKAGES(outfolder):
    rtools.write_PACKAGES(outfolder, type='win.bin')

def main(libfolder=LIBFOLDER, outfolder=OUTFOLDER, exec=ZEXEC):
    zipit(libfolder, outfolder, exec) #loops through packages creating folders
    create_PACKAGES(outfolder) # creates the PACKAGES file for R
    
if __name__ == '__main__':
    sys.exit(main())
