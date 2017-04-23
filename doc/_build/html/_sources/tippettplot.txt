.. _rst_tippetplot:

Tippett plot
============

Will plot a tippet plot showing the odds of a false positive and false negative
versus the raw scores. In order to draw the curves, the number of scores equal to or bigger than
a threshold are counted. This is done for a number of threshold values. The number can be set via
nrSamples4Probability in bioplot.cgf in section [probability]. The default is 250 steps.

Run this command: ::

    python ./bioplot.py -e "condition A and B" -i input/testdata_AB.txt -T

.. image:: images/condition_A_and_B_tippett_plot.png

If you want to see the cllr and cllrMin, nr of target and nontarget scores and eer values in the plot's legend, set: ::

    [roc]
    showCllr = True
    showMinCllr = True
    showCounts = True
    showEer = True

.. image:: images/condition_A_and_B_tippett_plot_all_metadata.png

If you want to print the plot to a file instead of to the screen, set printToFile accordingly.
The file name will be <experiment name>_tippett_plot.png. ::

        [cfg]
        printToFile = True
