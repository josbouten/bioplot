.. _rst_accuracy:

Accuracy plot
=============

This plot shows 2 accuracy measures for a range of decision thresholds: ::

    python ./bioplot.py -e "accuracy plot" -i input/testdata_A.txt -A

.. image:: images/test_accuracy_plot.png
   :alt: accuracy plot
   :align: left

The plot shows the random and the balanced accuracy for a range of threshold values.
In the plot the accuracy at the system's decision threshold is indicated. You can choose this via the command line option -d or - -threshold like so: ::

   python ./bioplot.py -e "accuracy plot" -i input/testdata_A.txt -A --threshold 0.7


This value obviously depends on the system under test. The number of target tests (#t) and the number of non target tests (#nt) is shown in the x-axis label.
The threshold value can be set via the command line option '-d' or the 'threshold' option. ::

                              number of true positives + number of true negatives
    random accuracy= -----------------------------------------------------------------------------
                     number of true positives + false positives + false negatives + true negatives


                        sensitivity + specificity        0.5 * true positives                   0.5 * true negatives
    balanced accuracy = -------------------------- = --------------------------------  +  ----------------------------------
                                    2                true positives + false negatives      true negatives + false positives
