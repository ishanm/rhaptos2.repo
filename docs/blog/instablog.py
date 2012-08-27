

"""
instablog
Just magically make sphonx into blog posts

generate a day or slugline and append that to the top of an index.rst file

  .. toctree::
     :maxdepth: 1

     20120723
     20120722
     how_I_did_it
     20120720
 

"""

import os
import sys
import datetime

def main():
    dt = datetime.datetime.today()
    f = os.path.join(FOLDER, "%s.rst" % dt.strftime("%Y%m%d"))
    prettydate = dt.strftime("%a, %d %b")
    open(f,'w').write("%s\n%s\n%s\n\n" % ("="*len(prettydate),
                                   prettydate, 
                                   "="*len(prettydate)
                                    ))
    
if __name__ == '__main__':
    FOLDER = "./"
    main()
