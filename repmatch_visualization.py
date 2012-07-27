import sys,os,math, numpy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable


usage = '''

input_paths may be:
- the output of rep-match statistics

example usages:
python repmatch_visualization.py /usr/local/repmatch_statistics.txt
'''.lstrip()

def run():
     
    if not len(sys.argv) == 2:
        print usage
        sys.exit(1)   
    
    width = 0.20
    infile = sys.argv[1]
    xlab = "Top x percentile peak-pair occupancy"
    ylab = "Percentage Reproducibility in >= 2 reps"
    plot =  os.path.join(os.path.dirname(os.path.abspath(infile)), "repmatch_visualization_bargraph.png")
    fig = Figure(figsize=(8,6))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
   
    #ax.set_aspect('auto',adjustable='box',anchor='C')
    # Set the X Axis label.
    ax.set_xlabel(xlab,fontsize=8)
    # Set the Y Axis label.
    ax.set_ylabel(ylab,fontsize=8)
    col = ['r', 'g', 'b', 'c']
    ind = numpy.arange(7)
    count = 0
    input = open(infile,'rt')
    for i in input:
        if not i.startswith("id"):
            no = i.rstrip().split("\t")
            newno = map(float,no[4:])
            rect1 =  ax.bar(ind,newno, width, color=col[count],label="Rep"+str(count+1))
            ind = ind+width
            count +=1
            #autolabel(rect1)
    
    ax.set_xticks(ind-width)
    ax.set_xticklabels(('1%tile', '5%tile', '10%tile','25%tile','50%tile','75%tile','100%tile'),size='x-small')
    ax.set_yticklabels((0,20,40,60,80,100))
    lfp = FontProperties()
    lfp.set_size('xx-small')
    ax.legend(loc=1,prop=lfp)
    canvas.print_figure(plot)
    
#def autolabel(rects):
#    # attach some text labels
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%float(height),
#                ha='center', va='bottom')


if __name__ == "__main__":
    run()

