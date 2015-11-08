.. _rst_rocplot:

ROC plot
========

Will plot a so called Receiver Operating Characteristic plot also known as ROC plot.
This plot shows the true positive versus the false positive rate.

Example command: ::

    python ./bioplot.py -e "condition A, B and C" -i input/testdata_ABC.txt -O

.. image:: images/condition_A_and_B_eer_plot.png

If you want to see cllr and cllrMin values in the plot's legend, set: ::

    [roc]
    showEerValues = True
    showCllrValues = True
    showCllrMinValues = True
