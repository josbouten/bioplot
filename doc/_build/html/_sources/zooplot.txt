.. _rst_zooplot:

Zoo plot
========
A zoo plot shows a scatter type plot where on the vertical axis the mean of the non target
scores and on the horizontal axis the mean target scores are drawn for each label. This leads to
a plot of dots where each dot represents the scores for one subject. The plot below shows an example with one dataset.
The zoo's special animals are coloured differently to make them stand out more.

Run this command: ::

    python ./bioplot.py -e "condition A" -f input/testdata_A.txt -Z

.. image:: images/condition_A_traditional_zoo_plot.png

You can combine multiple data sets in one plot. The next plot below shows combined data of 3 experiments (A, B and C).
The legend shows the eer and cllr values for the respective conditions.

Run this command: ::

    python ./bioplot.py -e "condition A, B and C" -f input/testdata_ABC.txt -Z

.. image:: images/condition_ABC_traditional_zoo_plot.png

An extention of the zoo plots was shown at the IAFPA 2014 conference in Zurich, Switserland
by Anil Alexander et al. They proposed that adding a measure of the standard deviations of the
scores used to make the plot will add details of the score distributions of the subjects
to the plot. If the option alexanderStyle in [zoo] is set to True, ellipses are drawn
at the positions where the points of a traditional zoo plot would be.
The width and height of the ellipses shown are essentially the standard deviations of the average
target and average non target scores for a given label. Because these may be much bigger or much
smaller than the horizontal and vertical scales of the traditional zoo plot, the mean standard
deviations are scaled by subtracting the overall mean standard deviation and dividing by the
standard deviation of all standard deviations. This is in essence a normalization procedure.
The result will be ellipses with a unit width and height and ellipses smaller and bigger than that.
To be able to actually plot the normalised ellipses, the width is multiplied by the range of
scores on the horizontal axis and the height is multiplied by the range of the scores on the vertical axis.
Finally to scale the ellipses their width and height is divided by a scale factor.
This scale factor is related to the number of pixels in the display used to plot the zoo plot.
A value of 150 works nicely for a 1600 ... 1280x1024 display.
To get this type of plot set the following option in your settings file: ::

    [zoo]
    alexanderStyle = True

.. image:: images/condition_ABC_alexander_zoo_plot.png

If you don't like the colors used, specify your own list in the section [metacolors] of the settings file.
Different colors make it possible to combine multiple data sets in one plot.
Note: don't use white or some very light colour as the plot's
canvas is white and you would not see much of a label then.
From a perceptual point you should avoide pure Blue
in combination with other colors as the human eye does not focus
blue light in the same way as the other colours because of chromatic aberation
when viewing multiple colours at the same time.
The meta data values are sorted alphabetically.
The colors are used in the sequence they are listed here.
Note that the labels are of no consequence! They are there for your convenience.
Values should be in R,G,B format specifying integer values
or hexadecimal values (6 digits). Search for color values on the web using 'html colors' as the search string
and you will find various lists and examples. ::

    [metacolors]
    IWouldCallThisBlueIsh = 3399FF
    Orangy = 255,125,10
    rustLike = 96,17,0
    someSortOfPink = 255,54,160
    OneOf50ShadesOfGrey = 10,5,8
    someWhatBlue = 1414FF
    definatelyGreen = 0,255,0
    definatelyRed = 255,0,0

Note that the shape of the ellipses is influenced by the difference in range of the vertical and
horizontal axis. This means that comparing shapes between zoo plots with varying ranges of
mean target and mean non target scores can be very tricky. The lines between the ellipses connect ellipses for the
same label.

Unit and mean reference
-----------------------
The grey/black ellipse in the center of the quartiles denotes the mean of all ellipses. The 3 red ellipses on the
lower left are meant as reference points. Their sizes measure (from smallest to largest ellipse): mean - 2
standard deviations, mean, mean + 2 standard deviations.

If you do not want these in your plot make the following setting. ::

    [zoo]
    showReference = False
    showUnitDataPoint = False


Highlighting labels
-------------------
If you click on a data point in the plot, a text label will be shown near the point. This makes
it possible to find the name of a data point in e.g. the quartile ranges.

If you are curious where the scores of a specific label are in the zoo plot, you need
not click on all of them to find it. You can specify the labels on the command line.
If they are in the plot, they will be highlighted. Example: ::

    python ./bioplot.py -e "condition A and B" -f input/testdata_AB.txt -Z 1100 1109 1042

This will highlight label 1100, 1109 and 1042 in the zoo plot compiled from
the data in 'testdata_AB.txt' and dim the colors of the other points in the plot
making it easy to create a picture for a publication or report. Text labels
will be displayed near the points selected.

.. image:: images/condition_A_and_B_not_interconnected_zoo_plot.png
   :alt: zoo plot for experiment with condition A and B

The lines between the ellipses connect labels which are equal. This makes
it easy to see what the effect of the parameter change is. ::

    [zoo]
    interconnectMetaValues = True


.. image:: images/condition_A_and_B_interconnected_zoo_plot.png
   :alt: zoo plot for experiment with condition A and B

Zooplots combined with Histograms
---------------------------------

In the plot shown below the zoo plot is bordered by histograms showing the distributions of the target and non target scores. In this zoo plot 2 data sets are shown combined. The points corresponding with one label are interconneted. To get bioplot to show this, set the following option in bioplot.cfg: ::

    [zoo]
    boutenStyle = True

.. image:: images/A_and_B_zoo_plot.png

The interface used to display the plots allows the user to zoom in on any part of the plots shown.

.. image:: images/condition_A_and_B_zoo_plot_zoom.png


