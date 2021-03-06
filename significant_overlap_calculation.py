import sys, os, pybedtools, math
from optparse import OptionParser , IndentedHelpFormatter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator
from matplotlib import patches

glist = []
pt95 = []


chrom = {'chr1':(1, 230208),'chr2':(1, 813178),'chr3':(1, 316617),'chr4':(1, 1531918),'chr5':(1,576869),'chr6':(1, 270148),'chr7':(1, 1090946),'chr8':(1, 562643),'chr9':(1, 439885),'chr10':(1, 745745),'chr11':(1, 666454),'chr12':(1, 1078175),'chr13':(1, 924429),'chr14':(1, 784333),'chr15':(1, 1091289),'chr16':(1, 948062),}

# Implementation of the method discussed in 
#  Negre et al. (2010) PLoS Genet 6(1): e1000814
# Requires, Scipy, Numpy and Pybedtools. Also requires a file
# sg07.txt conatining chromosome sizes.

    
def compare_all_by_all(files,sg07,options,outfile):
    Z = [] # The matrix of enrichment values
    i = 0
    nof = 0 # no of files in the folder aka..the order of matrix..3X3 oe 2X2 so on
    labels = [] # Stores the file names to be used in labels
    rect = []   # stores patch instances to be given as an argument to the legend() function
    for file1 in files:
        X = []
        i+=1
        labels.append(str(nof)+" => "+os.path.basename(file1))
        nof = nof +1
        rect.append(patches.Patch())
        for file2 in files:
            #print "Calculating actual overlap for "+ file1 +" and "+ file2
            z = calculate_overlap(file1,file2,sg07,options)
            X.append(z)
        Z.insert(i,X)
    draw_heatmap(Z,nof,labels,outfile,rect)
            
def calculate_overlap(file1,file2,sg07,options):
    
    try:
        results = pybedtools.BedTool(file2).set_chromsizes(chrom).randomstats(pybedtools.BedTool(file1).slop(g=sg07,l=options.down_distance,r=options.up_distance),iterations=options.iter,shuffle_kwargs={'chrom':True})
    except ImportError:
        print "Either Scipy or Numpy or pybedtool is not installed in your system!"
    
    ###pvalue = calculate_emperical_pvalue(observed_c1_and_f2,results,options.iter)
    #print results['actual']
    
    pt95.append(results['upper_97.5th'])
    if math.isinf(results['normalized']):
        glist.append(0)
        sys.stderr.flush()
        return(0)
        
        
    else:
        glist.append(results['normalized'])
        sys.stderr.flush()
        return(results['normalized'])
    
        
    
    
    
def draw_heatmap(vals,nof,labels,outfile,rect):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    bounds =  np.linspace(min(glist),max(glist))
    norm = cl.BoundaryNorm(bounds, ncolors=256, clip = False)
    pt = ax.imshow(np.asarray(vals),cmap=cm.get_cmap('gist_rainbow'),norm=norm,interpolation='nearest')
    #pt = ax.imshow(np.asarray(vals),cmap=cm.get_cmap('Blues'),vmin=min(glist),vmax=max(glist),interpolation='nearest')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right",size="5%",pad=0.05)
    plt.colorbar(pt,cax=cax,drawedges=False)
    ax.xaxis.set_major_locator(MaxNLocator(nof+1))
    ax.yaxis.set_major_locator(MaxNLocator(nof+1))
    lfp = FontProperties()
    lfp.set_size('xx-small')
    ax.legend(rect,labels,prop=lfp,bbox_to_anchor=(0,1,1.,.1),loc=9,borderaxespad=0.)
    plt.savefig(outfile)
    print "The matrix of enrichment scores"
    print np.asarray(vals)
    
    
    
#def calculate_emperical_pvalue(observed,results,i):
#    count = 0
#    for exp in results:
#        if exp > observed:
#            count+=1
#    print count
#    return(float(count/i))


usage = '''
input_paths may be:
- a directory to run on all files in them

example usages:
python significant_overlap_calculation.py /usr/local/peak-pairs/
'''.lstrip()


 
# We must override the help formatter to force it to obey our newlines in our custom description
class CustomHelpFormatter(IndentedHelpFormatter):
    def format_description(self, description):
        return description


def run():
    parser = OptionParser(usage='%prog [options] input_paths', description=usage, formatter=CustomHelpFormatter())
    parser.add_option('-u', action='store', type='int', dest='up_distance',default=49,
                      help='Upstream distance to go from the peak-pair mid_point+1, Default=49.')
    parser.add_option('-d', action='store', type='int', dest='down_distance',default=50,
                      help='Downstream distance to go from the peak-pair mid_point, Default=50')
    parser.add_option('-i', action='store', type='int', dest='iter',default=100,
                      help='Number of iterations to do for shuffling')
    
    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
        sys.exit(1)
        
    outfile = os.path.join(args[0],"Heatmap")    
    files = []
    if not os.path.exists(args[0]):
        parser.error('Path %s does not exist.' % args[0])
    for name in os.listdir(args[0]):
        if name.startswith('S_'):
            fname = os.path.join(args[0], name)
            files.append(fname)
        if name.startswith('sg07'):
            sg07 = os.path.join(args[0], name)
        #if name.startswith('Around'):
        #    comp = os.path.join(args[0],name)
    #compare_all_by_all(files,sg07,comp,options,outfile)
    compare_all_by_all(files,sg07,options,outfile)
    
    
if __name__ == "__main__":
    run() 