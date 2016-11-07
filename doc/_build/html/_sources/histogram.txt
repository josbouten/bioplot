.. _rst_histogram:


Histogram
=========

A histogram can be used to view the distribution of target and non target scores.

Run this command to see an example: ::

    python ./bioplot.py -e "condition A" -i input/testdata_A.txt -H

.. image:: images/condition_A_histogram_plot.png

The window showing the plot allows you to zoom in as shown in this example:

.. image:: images/condition_A_histogram_plot_detail.png

Normalization
-------------
By default the bins of the datasets shown in the histogram are normalized. Especially with large differences in numbers
this makes it possible to see the score ranges of the target and non target scores. Otherwise the target scores in particular
might not be clearly visible. If you do not want this, set normHist to False: ::

    [histogram]
    normHist = False

.. image:: images/condition_A_histogram_not_normalized_plot.png

Number of bins
--------------
You can set the  number of bins. Either specify a number or rice, sqrt or sturges.
See https://en.wikipedia.org/wiki/Histogram#Number_of_bins_and_width ::

    [histogram]
    nrBins = 150

Combined experiments
--------------------
Obviously you can also visualize combined experiments. Here is an example of the command. The plot shows a region
of the histogram after zooming in: ::

    python ./bioplot.py -e "condition A and B" -i input/testdata_AB.txt -H

.. image:: images/condition_AB_histogram_plot_detail.png

If you are interested in a cumulative plot, have a look at :ref:`rst_eerplot`.

If you want to print the plot to a file instead of to the screen, set printToFile accordingly.
The file name will be <experiment name>_histogram.png. ::

        [cfg]
        printToFile = True
