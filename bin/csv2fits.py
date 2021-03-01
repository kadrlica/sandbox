#!/usr/bin/env python
"""
Convert from CSV format to FITS format.
"""
__author__ = "Alex Drlica-Wagner"
import os.path
import fitsio
import pandas as pd

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filenames',nargs='+',
                        help='input name(s) of CSV file(s)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l','--lower',action='store_true',
                       help='lowercase column names')
    group.add_argument('-u','--upper',action='store_true',
                       help='uppercase column names')
    parser.add_argument('-f','--fpack',action='store_true',
                        help='fpack output FITS files')
    parser.add_argument('-v','--verbose',action='store_true',
                        help='output verbosity')
    parser.add_argument('-z','--gzip',action='store_true',
                        help='gzip output FITS files')
    args = parser.parse_args()

    extensions = ['.csv']
    compress   = ['','.gz']

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

        outfile = outbase + '.fits'
        if args.gzip:  outfile += '.gz'
        if args.fpack: outfile += '.fz'
        
        if args.verbose: print("Reading %s..."%filename)
        data = pd.read_csv(filename)

        if args.upper:
            data.columns = map(str.upper,data.columns)
        elif args.lower:
            data.columns = map(str.lower,data.columns)
        data = data.to_records(index=False)

        if args.verbose: print("Writing %s..."%outfile)
        fitsio.write(outfile,data,clobber=True)
        
        
