'''This script points to an R library directory (LIBFOLDER) where built R
packages are (non-zipped) and creates an R package repositiory in the
output directory (OUTFOLDER).

LIBFOLDER and OUTFOLDER can be passed as arguments:
python R_pkg_builder.py LIBFOLDER=/usr/lib/R/library OUTFOLDER=$(pwd)

The zip files and the PACKAGES file this script creates in the output
directory can be used in R's install.packages() function, as in:
install.packages(repos='path to repo', type='win.bin')
'''

import os, sys
import zipfile
from rpy2.robjects.packages import importr


class RPkgr():
    def __init__(self, LIBFOLDER=None, OUTFOLDER=None):
        '''Pulls variables in from passed arguments. Also allows
           user to pass when creating instance.'''
        if len(sys.argv) > 1:
            for arg in sys.argv[1:len(sys.argv)]:
                try:
                    k,v = arg.split('=')
                    v = v.replace('\\','/') # change windows to unix style
                    exec('self.'+k.upper()+'='+"\'"+v+"\'")
                except:
                    pass
        try:
            assert(type(self.LIBFOLDER) == str)
        except Exception as e:
            raise TypeError("LIBFOLDER not specified, or not a string: {}".format(e))
        try:
            assert(type(self.OUTFOLDER) == str)
        except Exception as e:
            raise TypeError("OUTFOLDER not specified, or not a string: {}".format(e))

    def extract_version(self, file):
        '''Return version number from an R Description file.
           Example:
           extract_version('/usr/lib/R/library/base/DESCRIPTION')'''
        stream = open(file, 'r').read().replace('\t','').split('\n')
        d = {}
        for x in stream:
            try:
                k,v = x.split(':')
                d[k] = v
            except: pass # not all lines can be parsed, which is fine
        version = d['Version'].strip() # we just need the Version line
        return version

    def zipit(self):
        '''for each package in LIBFOLDER, extracts version number
           to use in naming a zip file. Zips package to OUTFOLDER
           in correct format.'''
        comp_lev = zipfile.ZIP_DEFLATED
        for dir in os.listdir(self.LIBFOLDER):
            try:
                libpath = os.path.join(self.LIBFOLDER, dir, 'DESCRIPTION')
                v = self.extract_version(libpath)
                zfile_name = self.OUTFOLDER+'/'+dir+'_'+v+'.zip'
                if not os.path.isfile(zfile_name): # don't overwrite if exists
                    zipf = zipfile.ZipFile(zfile_name, 'w', comp_lev)
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            zipf.write(os.path.join(root, file))
                    zipf.close()
                    print('Successfully zipped {}'.format(dir))
            except Exception as e:
                print('Cannot zip {0}: {1}'.format(dir, e))

    def create_PACKAGES(self):
        '''Call R tools::write_PACKAGES function to create
           PACKAGES file needed for repo'''
        try:
            self.zipit()
            rtools = importr('tools')
            rtools.write_PACKAGES(self.OUTFOLDER, type='win.bin')
            return 0
        except Exception as e:
            print(e)
            return 1

    
if __name__ == '__main__':
    pkgr = RPkgr()
    sys.exit(pkgr.create_PACKAGES())
