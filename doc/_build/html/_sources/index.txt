.. bioplot documentation master file, created by
   sphinx-quickstart on Fri Oct 24 21:48:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bioplot's documentation!
===================================

Contents:

.. toctree::
   :maxdepth: 2

   install
   update
   accuracy
   eerplot
   histogram
   matrixplot
   rankingplot
   tippettplot
   zooplot
   tools
   settings
   issues

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
=======

Copyright (C) 2014, 2015 Jos Bouten ( josbouten at gmail dot com )

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

bioplot
=======
You will not be able to use this program or any of its parts to slay a dragon, that
I'm sure of, and I do not guarantee that it is fit for any other purpose at all, but
I would appreciate if you would include a reference to this code and my name
in any publications you may write using it's features or add a source reference
to your code if you include some part(s) of this code in yours.

bioplot.py is a program which can draw several plots that can be used
when evaluating the performance of a biometric system. It reads settings from the file 'bioplot.cfg'.
But using the -f option you can specify your own settings file.
These settings may be used to determine the way information is shown in a plot, what directory plot files
are written to etc.

The plot types currently supported are:
accuracy plot, cumulative score distribution plot, EER plot, histogram, matrix plot,
ranking plot, tippett plot and zoo plot.

Please read INSTALL.txt, this html documentation (note that the file 'manual.txt' is obsolete) and bioplot.cfg before you try to use
'bioplot.py'. You'll learn more of the program's potential than from its command line help message.

@Windows dudes and dudettes: I'm afraid you have to run the program by hand from
a command line or build shortcuts which not only start the program but also
provide the command line options and parameters needed. You're on your
own here. I'm a command line junky anyway so I did not spend any
time building a gui. But don't fret. All plots ares shown in an interactive
window, you can click on that as much as you like. The interface
allows you to zoom in, click on a point to see the associated label, save
the plot in a file etc. etc.

What bioplot.py basically does is: read a data file and plot an interactive graph.
There is a choice to be made what type of graph you want. 
The data has to be in a specific format. Actually there are 3 types of 
format allowed. See 'Data Files' below. All plots can be saved. This happens
automagically as well, but you get more useful results if this happens under 
your control.

The program does a bit more than its command line arguments suggest.
You will notice this when you run it. It will for instance store all the
target and non target scores it distills from the data file you pass
to it and write them in text files (unless you set saveScores to False in bioplot.cfg). You can use these for further
processing. The experiment name you specify is used as part
of the filename: <exp_name>_<meta_value>_non_target.txt, <exp_name>_<meta_value>_target.txt.
The files are stored in the directory specified by 'outputPath' in
bioplot.cfg in it's [cfg] section. The default will be 'output' in
the current directory. You can change this behaviour in bioplot.cfg via the following settings: ::

   [cfg]
   outputPath = output
   saveScores = True
   alwasySave = False

If you run the program again using the same experiment
name, the scores are not saved anew, saving some processing time, unless you set alwaysSave = True in [cfg].
The default value is False as it is expected that you will run bioplot several times with the same data.
If you want to have new versions of these files, you need to delete
them before running bioplot.py again.

Next, if you choose to plot a zoo plot, the labels which fall within the
doves, chameleons, worms and phantom quartiles are saved in individual
text files: <exp_name>_chameleons.txt, <exp_name>_doves.txt,
<exp_name>_phantoms.txt and <exp_name>_worms.txt.
This automatically documents all outliers.

The labels with a standard deviation for their target scores or their
non target scores bigger than the unit standard deviation are stored
in a file <exp name>_limited.txt together with the violating score (have a look
at the :ref:`rst_zooplot` page for a general understanding of how the plot is made).

Example: ::

  cat output/condition_A_limited.txt

  1096 target std dev: 6.01978718893
  335 non target std dev: 6.71906032808

Note that you can switch limiting on or off via setting limitStdDevs = False in bioplot.cfg section [zoo].

Any plot you produce will be saved to disk as soon as you click on
the plot (to het the window focus) and press a key.
Note, it is important to maximise the plot's window to get a
proper layout of all elements in the plot! If you maximise and
press 's', you will be presented with a menu which will allow you
to save the plot anywhere you choose to.
If you press a different key, the plot will be saved locally in
the directory specified by outputPath.
This happens any time you press a key except l, k, g, s, f:

Note: l, k, g, s and f are predefined keys of the gui.
With them you can: ::

  g: toggle grid on / off
  k: toggle between lin horizontal scale and log horizontal scale
  l: toggle between lin vertical scale and log vertical scale
  s: open save menu
  f: toggle between standard size and full screen

Any other key will make that the file is saved in its current dimensions.
To get a nice plot it is wise to maximise and then press any key. Then close
the window.

Data files
==========
The command line allows to specify a filename and a type. The 
default type is 'type3' which corresponds to a text file with 7 fields. You need
not specify type3 as it is a default.
The type3 data file should contain data in a format like this example: ::

    803742 17133729a.wav 803593 16842970b.wav 2.108616847991943 FALSE META_VAL1
    148407 47968376b.wav 898232 08087650a.wav 0.336018745422363 FALSE META_VAL3
    179408 34192626a.wav 803721 16749939b.wav 1.263523664188385 FALSE META_VAL2
    803442 48588750a.wav 803442 15560933b.wav 4.423274517059326 TRUE  META_VAL2

Separation by comma's is also accepted.
This can be mixed as in: ::

    803742,17133729a.wav,803593,16842970b.wav,2.108616847991943,FALSE,META_VAL1
    148407,47968376b.wav,898232,08087650a.wav,0.336018745422363,FALSE,META_VAL3
    179408 34192626a.wav 803721 16749939b.wav 1.263523664188385 FALSE META_VAL2
    803442,48588750a.wav,803442,15560933b.wav,4.423274517059326,TRUE, META_VAL2

field 1: string: label identifying a subject (training data).

field 2: string: name of data file containing biometric features or raw data originating from the subject denoted by field 1 used for making a test model. In the example you see a wav-file, but this can be any string identifying a file or feature set. 

field 3: string: label identifying a subject (test data).

field 4: string: name of data file containing biometric features or raw data originating from the subject denoted by field 3 used for training the reference model. In the example you see a wav-file, but this can be any string identifying a file or feature set.                            

field 5: string: floating point value: score of trial.

field 6: boolean: ground truth.

field 7: meta data value for the experiment.

Field 7 can be used to contrast scores of experiments in most plots.

So if you have 2 experiments where you change one variable, when doing a cross
identification test, the meta value can be used to group the experiment's scores.

E.g. you run an experiment with gender as the main variable and you collect scores of male
to male and female to female comparisons. You need to set the meta value for each score 
accordingly. The meta value field allows bioplot to distinguish
between the two conditions and it will in essence plot 2 plots in one overview.
If the same label occurs on more than one occasion in the score list with different meta
values, then the points in a zoo plot with corresponding labels are interconnected 
(see interconnectMetaValues setting in bioplot.cfg under [zoo]) . This makes it easy
to see what the effect of an individual label is when changing the experiment's condition.

Field 7 must be present. If you don't want to contrast experiments, then give all lines
the same meta value. Any string of characters (excluding white space) will do except 
the special characters mentioned below under 'Known Issues'.

File type 'type2' is deprecated as of august 2015.

File 'type1' is a database based data format and meant as an example on how to use bioplot in combination with a
database of scores. Specify 'database' as filename on the command line.

Example: ::

  python ./bioplot.py -f database -t type1 -e 'data taken from db' -Z

You will have to adapt the query in the function _readFromDatabase and the function
_decodeType1Results in data.py to your own needs.

There are 4 data files (of type3) which are meant as examples to play around
with: testdata_A.txt, testdata_B.txt, testdata_C.txt and testdata_ABC.txt

Example: ::

  python ./bioplot.py -e "condition A" -f testdata_A.txt -Z

If you experience any difficulties reading your data file, we can either discuss this
via email or you can send it to me ( josbouten at gmail dot com ) so that I can have a look at it.
Please consider anonimizing the data before you send it to me by mail! Have a look at
anonimize.py and adapt it to your needs.


Finally:

If you have any questions or feature requests (no guarantees!) or find any bugs,
you can contact me at josbouten at gmail dot com.
