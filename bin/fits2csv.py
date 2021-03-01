#!/usr/bin/env python
"""
Convert from FITS format to CSV.
"""
__author__ = "Alex Drlica-Wagner"
import os.path
import fitsio
import pandas as pd

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames',nargs='+',
                        help='input name(s) of FITS files')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l','--lower',action='store_true',
                       help='lowercase column names')
    group.add_argument('-u','--upper',action='store_true',
                       help='uppercase column names')
    parser.add_argument('-v','--verbose',action='store_true',
                        help='output verbosity')
    parser.add_argument('-z','--gzip',action='store_true',
                        help='gzip output CSV files')
    args = parser.parse_args()

    extensions = ['.fit','.fits']
    compress   = ['','.gz','.fz']

    for filename in args.filenames:
        basename = os.path.basename(filename)

        outbase = None
        for ext in extensions:
            for comp in compress:
                suffix = ext+comp
                if basename.endswith(suffix):
                    outbase = basename.replace(suffix,'')
                    break
            if outbase: break
        else:
            msg = "Unrecognized file extension: %s"%filename
            raise IOError(msg)

        outfile = outbase + '.csv'
        if args.gzip: outfile += '.gz'
        
        if args.verbose: print("Reading %s..."%filename)
        data = fitsio.read(filename)
        data = pd.DataFrame(data.byteswap().newbyteorder())

        if args.upper:
            data.columns = map(str.upper,data.columns)
        elif args.lower:
            data.columns = map(str.lower,data.columns)

        if args.verbose: print("Writing %s..."%outfile)
        data.to_csv(outfile,index=False,compression='gzip' if args.gzip else None)
        
        
