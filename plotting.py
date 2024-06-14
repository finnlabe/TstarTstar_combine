import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

def plotGoodnessOfFit(file_data, file_toys, xlim=[0, 250], xbins=20):
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # file_data contains a histogram with one entry
    with uproot.open(file_data) as file:
        array_data = file["limit/limit"].array()
        assert( len(array_data) == 1 )
        value_data = array_data[0]
        
    with uproot.open(file_toys) as file:
        array_toys = file["limit/limit"].array()
        
        
    # calculate p-value
    p_value = np.count_nonzero( array_toys > value_data ) / len(array_toys)
        
    # generate histogram
    hist_data, bist_bins = np.histogram(array_toys, bins = xbins)
        
    # plot histogram and arrow
    hep.histplot(hist_data, bist_bins, color="black", ax=ax)
    ax.arrow(value_data, np.max(hist_data)*0.1, 0, -np.max(hist_data)*0.1, width=(xlim[1] - xlim[0])/50, head_width=(xlim[1] - xlim[0])/25, head_length=np.max(hist_data)*0.05, length_includes_head=True )
    
    # plot line for text at top
    ax.plot( [xlim[0], xlim[1]], [np.max(hist_data)*1.1, np.max(hist_data)*1.1], color="black", linewidth=.75)
    
    # plot text
    text = "saturated, " + str(len(array_toys)) + " toys,\np-value = " + str(p_value)
    ax.text((xlim[1] + xlim[0])/2, np.max(hist_data)*1.2, text,
        horizontalalignment='center',
        verticalalignment='center')
    
    # styling
    ax.set_ylim(0, np.max(hist_data)*1.3)
    ax.set_xlim(xlim[0], xlim[1])
    
    
# function to plot another line
# expects a dictionary, where the keys are x and the content is y
# content may be one or two numbers, the second being an uncertainty
def plot_other_line(line, label, ax, linestyle=None, linewidth=None,color=None, plotUncertainty=False):
    
    x = list(line.keys())
    y = []
    err = []
    
    for x_ in x:
        y_tot = line[x_]
        y.append(y_tot[0])
        if(len(y_tot)>1): err.append(y_tot[1])
       
    # plotting the line
    ax.plot(x, y, label = label, linestyle = linestyle, linewidth=linewidth, color=color)

    if plotUncertainty and len(y_tot) > 1:
        # plotting error band
        lows = [y - error for y, error in zip(y, err)]
        highs = [y + error for y, error in zip(y, err)]

        ax.fill_between(x, lows, highs, color = color, alpha=0.5)
       
    
def plot_skeleton(year = None, text = "", data=False, figsize=(10, 10)):
    
    if (year == "UL18"): lumi = 59.83
    elif (year == "UL17"): lumi = 41.48
    elif (year == "UL16"): lumi = 36.31
    elif (year == None): lumi = 138
        
    if year: year = year.replace("UL", "20")
        
    fig, ax = plt.subplots(figsize=figsize)
    hep.cms.label(text, lumi=lumi, year=year, data=data, loc=1)
    
    return fig, ax