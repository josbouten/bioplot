Histogram
=========

Nothing much to say about histograms. Here is an example:

Run this command: ::

    python ./bioplot.py -e "condition A" -f input/testdata_A.txt -H

.. image:: images/condition_A_histogram_plot.png

You can set the  number of bins used in bioplot.cfg: ::

    [histogram]
    nrBins = 150

The window showing the plot allows one to zoom in as shown in this example:

.. image:: images/condition_A_histogram_plot_detail.png

If you are interested in a cumulative plot, have a look at :ref:`eerplot-label`.
