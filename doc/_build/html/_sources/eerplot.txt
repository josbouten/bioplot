.. _rst_eerplot:

EER plot
========

Will plot a cumulative score plot showing the odds of a false positive and false negative
versus the raw scores. In order to draw the curves, the number of scores equal to or bigger than
a threshold are counted. This is done for a number of threshold values. The number can be set via
nrSamples4Probability in bioplot.cgf in section [probability]. The default is 250 steps.
The EER is calculated as the point in a cumulative score plot where the line showing the target scores crosses the line for the non target scores.
The data points nearest to the crossing point are used and the crossing point is computed via interpolation.

Example command: ::

    python ./bioplot.py -e "condition A and B" -i input/testdata_AB.txt -E

.. image:: images/condition_A_and_B_eer_plot.png

All plots are shown in a window that allows you to zoom in on events. Here the plot is zoomed in around the intersection points of the graphs.

.. image:: images/condition_A_and_B_eer_plot_zoom.png

If you want to see cllr and cllrMin values in the plot's legend, set: ::

    [eer]
    showCllr = True
    showMinCllr = True

.. image:: images/condition_A_and_B_eer_plot_cllr.png

If you want to print the plot to a file instead of to the screen, set printToFile accordingly. 
The file name will be <experiment name>_eer_plot.png. ::

	[cfg]
	printToFile = True
