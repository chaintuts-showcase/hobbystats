# This file contains code for visualizing data computed by the core hobbystats modules
#
# Author: Josh McIntyre
#
import argparse
import csv
import datetime
import numpy
import matplotlib
from matplotlib import pyplot
import dateutil

# This function plots a graph
def graph_stats_bar(data, title, xlabel, ylabel):

    # Set up the basic plot
    dimensions = matplotlib.figure.SubplotParams(left=0.05, right=0.9)
    fig, ax = pyplot.subplots(subplotpars=dimensions)

    # Generate the data and labels for the chart
    xlabels = [ key for key, value in data.items() ]
    x = range(1, len(xlabels) + 1)
    
    y = [ float(value) for key, value in data.items() ]

    # Plot the bar chart
    bars = ax.bar(x, y, linewidth=1)

    # Add annotations
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, rotation=90)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)

    pyplot.title(title)

    # Render the chart
    pyplot.tight_layout()
    pyplot.show()
    return fig, ax

