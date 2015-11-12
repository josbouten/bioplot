.. _rst_rankingplot:

Ranking plot
============

Bioplot.py allows you to plot a ranking plot. Example run: ::

    python ./bioplot.py -e 'exp AB' -i input/testdata_AB.txt -R

E.g. if looking for a picture in a database a face recognition system may return a list of potential hits. This plot shows what the odds are that the target will be in the first N pictures.

.. image:: images/exp_AB_ranking_plot.png
