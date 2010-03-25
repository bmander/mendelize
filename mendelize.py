#!/usr/bin/python

import re

def path_from_gcode( fp ):
    
    for line in fp:
        
        match = re.match( "G00X(.*)Y(.*)Z(.*)", line )
        if match:
            groups = match.groups()
            yield (float(groups[0]), float(groups[1]), float(groups[2]))
            continue
            
        match = re.match( "G00Z(.*)", line )
        if match:
            yield (None, None, float(match.groups()[0]))
            continue
            
        match = re.match( "X(.*)Y(.*)", line )
        if match:
            groups = match.groups()
            yield (float(groups[0]), float(groups[1]), None)
            continue
            
        match = re.match( "Z(.*)", line )
        if match:
            yield (None, None, float(match.groups()[0]))
            continue
            
        match = re.match( "G01Z(.*)", line )
        if match:
            yield (None, None, float(match.groups()[0]))
            continue
            
def mendel_gcode_from_path( path, toolup=0.5, zfeedrate=30, xyfeedrate=300 ):
    for x,y,z in path:
        if x is None and y is None and z is not None:
            print "G1 F%d"%zfeedrate
            if z==0:
                print "G1 Z0"
            elif z>0:
                print "G1 Z%0.4f"%toolup
            print "G1 F%d"%xyfeedrate
        else:
            print "G1 X%0.4f Y%0.4f"%(x,y)

from optparse import OptionParser
def main():
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage)
    parser.add_option("-t", "--toolup", dest="toolup", default=0.5,
                      help="length to rise tool on toolup")
    parser.add_option("-z", "--zrate", dest="zrate", default=30,
                      help="z feedrate")
    parser.add_option("-f", "--xyrate", dest="xyrate", default=300,
                      help="x and y feedrate")
    
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    fp = open( args[0] )
        
    mendel_gcode_from_path( path_from_gcode( fp ), toolup=float(options.toolup),
                            zfeedrate=float(options.zrate), xyfeedrate=float(options.xyrate) )
                            
if __name__=='__main__':
    main()
