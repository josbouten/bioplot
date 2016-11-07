.. _rst_rocplot:

ROC plot
========

Will plot a so called Receiver Operating Characteristic also known as ROC plot.
This plot shows the true positive rate versus the false positive rate.

Example command: ::

    python ./bioplot.py -e "condition A, B and C" -i input/testdata_ABC.txt -O

.. image:: images/condition_ABC_roc.png

If you want to see EER, Cllr and/or MinCllr values in the plot's legend, set: ::

    [roc]
    showEer = True
    showCllr = True
    showMinCllr = True

If you want to print the plot to a file instead of to the screen, set printToFile accordingly.
The file name will be <experiment name>_roc_plot.png. ::

        [cfg]
        printToFile = True
