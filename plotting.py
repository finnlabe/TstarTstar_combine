import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

def plotGoodnessOfFit(file_data, file_toys, xlim=[0, 250]):
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
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
    hist_data, bist_bins = np.histogram(array_toys)
        
    # plot histogram and arrow
    hep.histplot(hist_data, bist_bins, color="black", ax=ax)
    ax.arrow(value_data, np.max(hist_data)*0.1, 0, -np.max(hist_data)*0.1, width=(xlim[1] - xlim[0])/50, head_width=(xlim[1] - xlim[0])/25, head_length=np.max(hist_data)*0.05, length_includes_head=True )
    
    # plot line for text at top
    ax.plot( [xlim[0], xlim[1]], [np.max(hist_data)*1.1, np.max(hist_data)*1.1], color="black", linewidth=.75)
    
    # plot text
    text = "saturated, " + str(len(array_toys)) + " toys,\np-value = " + str(p_value)
    ax.text(xlim[1]/2, np.max(hist_data)*1.2, text,
        horizontalalignment='center',
        verticalalignment='center')

    
    # styling
    ax.set_ylim(0, np.max(hist_data)*1.3)
    ax.set_xlim(xlim[0], xlim[1])
    hep.cms.label("Internal")