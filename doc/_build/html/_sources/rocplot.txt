.. _rst_rocplot:

ROC plot
========

Will plot a so called Receiver Operating Characteristic also known as ROC plot.
This plot shows the true positive rate versus the false positive rate.

Example command: ::

    python ./bioplot.py -e "condition A, B and C" -i input/testdata_ABC.txt -O

.. image:: images/condition_ABC_roc.png

If you want to see the cllr and cllrMin, nr of target and nontarget scores and eer values in the plot's legend, set: ::

    [roc]
    showCllr = True
    showMinCllr = True
    showCounts = True
    showEer = True

.. image:: images/condition_ABC_roc_all_metadata.png

If you want to print the plot to a file instead of to the screen, set printToFile accordingly.
The file name will be <experiment name>_roc_plot.png. ::

    [cfg]
    printToFile = True
