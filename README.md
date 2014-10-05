manual.txt
Copyright (C) 2014 Jos Bouten ( josbouten@gmail.com )

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


You will not be able to use this program or any of its parts to slay a dragon, that
I'm sure of, and I do not guarantee that it is fit for any other purpose at all, but
I would appreciate if you would include a reference to this code and my name
in any publications you may write using it's features or add a source reference
to your code if you include some part(s) of this code in yours.

Please read INSTALL.txt, this manual and bioplot.cfg before you try to use
'bioplot.py'. You'll learn more of the program's potential than from its command
line help message.

@Windows dudes and dudettes: I'm afraid you have to run the program by hand from
a command line or build shortcuts which not only start the program but also
provide the command line options and parameters needed. You're on your
own here. I'm a command line junky anyway so I did not spend any
time building a gui. But don't fret. All plots ares shown in an interactive
window, you can click on that as much as your heart's desire. The interface
allows you to zoom in, click on a point to see the associated label, save
the plot in a file etc. etc.

What the program basically does is: read a data file, plot a graph and save
it in a file. There is a choice to be made what graph you want. 
The data has to be in a specific format. Actually there are 3 types of 
format allowed. See 'Data Types' below. All plots can be saved. This happens
automatically as well, but you get more useful results if this happens under 
your control.

The program does a bit more than its command line arguments suggest.
You will notice this when you run it. It will for instance store all the
target and non target scores it distills from the data file you pass
to it and write them in text files. You can use these for further
processing. The experiment name you specify is used as part
of the filename: <exp_name>_non_target.txt, <exp_name>_target.txt.
The files are stored in the directory specified by 'outputPath' in
bioplot.cfg in it's [cfg] section. The default will be 'output' in
the current directory.

If you run the program again using the same experiment
name, the scores are not saved anew, saving some processing time.
If you want to have new versions of these files, you need to delete
them before running bioplot.py again.

Next, if you choose to plot a zoo plot, the labels which fall within the
doves, chameleons, worms and phantom quartiles are saved in individual
text files: <exp_name>_chameleons.txt, <exp_name>_doves.txt,
<exp_name>_phantoms.txt and <exp_name>_worms.txt
This automatically documents all outliers.

The labels with a standard deviation for their target scores or their
non target scores bigger than the unit standard deviation are stored
in a file <exp name>_limited.txt together with the violating score.

Example: cat output/condition_A_limited.txt

1096 target std dev: 6.01978718893
335 non target std dev: 6.71906032808

Note that you can switch limiting on or off via setting
limitStdDevs = False in bioplot.cfg section [zoo].


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
With them you can:
g: toggle grid on / off
k: toggle between lin horizontal scale and log horizontal scale
l: toggle between lin vertical scale and log vertical scale
s: open save menu
f: toggle between standard size and full screen
any other key will make that the file is saved in its current dimensions.
To get a nice plot it is wise to maximise and then press any key. Then close
the window.

Data files
==========
The command line allows to specify a filename and a type. The type
by default is 'type3' which corresponds to a text file with 8 fields. You need
not specify type3 as it is a default.
The type3 data file should look like this:

803742 17133729a.wav 80359 16842970b.wav 2.108616847991943 FALSE META_VAL1
148407 47968376b.wav 89823 08087650a.wav 0.336018745422363 FALSE META_VAL3
179408 34192626a.wav 80372 16749939b.wav 1.263523664188385 FALSE META_VAL2
803442 48588750a.wav 80344 15560933b.wav 4.423274517059326 TRUE META_VAL2
etc.

The fields are separated by a space.
field 1: string: label identifying a person (training data)
field 2: string: name of data file containing biometric features or raw data originating
                 from the person denoted by field 1 used for makeing a test model.
                 In the example you see a wav-file, but this can be any string
                 identifying a file. 
field 3: string: label identifying a person (test data)
field 4: string: name of data file containing biometric features or raw data originating
                 from the person denoted by field 3 used for training the reference model.
                 In the example you see a wav-file, but this can be any string
                 identifying a file.                                 
field 5: string: floating point value: score of trial
field 6: string: meta data value for the experiment
Field 6 can be used to contrast scores of experiments in the zoo plot.
So if you have 2 experiments where you change one variable, when doing a cross
identification test, the meta value can be used to group the experiment's scores.

E.g. you run an experiment with gender as the main variable an you collect scores of male
to male and female to female comparisons. You need to set the meta value for each score
score accordingly. The meta value fields allow bioplot to distinguish
between the two conditions and it will in essence plot 2 zoo plots in one overview.
If the same label occurs on more than one occasion in the score list with different meta
values, e.g. in an experiment where the variable would be duration of training segment,
then the points in the plot with corresponding labels are interconnected. This makes it easy
to see what the effect of an individual label is when changing the experiment's condition.

Field 6 must be present. If you don't want to contrast experiments, then give all scores
the same meta value. Anything will do except the special characters mentioned below under
'Known Issues'.

File type 'type2' is a variant of a file based data format:

62124-0 62124-1 0.383234709501 META_VAL1
62124-0 62124-3 0.325683742762 META_VAL1
62124-0 80491-2 0.239269435406 META_VAL2
62124-0 64568-2 0.19219391048 META_VAL1
62124-0 64568-3 0.125796630979 META_VAL1
62124-0 77223-1 0.0895956531167 META_VAL2

In this format basically format type3's field 1 and 2 are combined into one field.
The same goes for field 3 and 4. You can use the corresponding code to adapt to your specific
data file format OR write some code to map it to a type3 format file.

File 'type1' is a database (sqlite) based data format and meant as an example on how to
use bioplot in combination with a database of scores. Specify 'database' as filename on the
command line.

Example:

python ./biplot -f database -t type1 -e 'data taken from db' -z

Obviously you have to adapt the query in data.py to your own needs.

There are 3 data files (of type3) which are meant as examples to play around
with: testdata_A.txt, testdata_B.txt, testdata_all.txt

Example:
python ./bioplot.py -e "condition A" -f testdata_A.txt -Z

If you experience any difficulties reading your data file, we can either discuss this
via email or you can send it to me ( josbouten@gmail.com ) so that I can have a look at it.
Please consider anonimizing the data before you send it to me by mail! Have a look at
anonimize.py and adapt it to your needs.

Highlighting labels
===================
If you are curious where the results of a given label are in the zoo plot,
you can specify them on the command line. If they are in the plot, they will
be highlighted, e.g.:

python ./bioplot.py -e "condition A" -f testdata_A.txt -Z 1130 1062 226

This will highlight label 1130 and 1062 and 226 in the zoo plot compiled from
the data in 'testdata_A.txt'.

If you want to see the combined results of experiments with the same
dataset but with some change in parameters, try the dataset which
combines the 'A' and 'B' experiment:

python ./bioplot.py -e "exp A vs B" -f testdata_all.txt -Z

The lines between the ellipses connect labels which are equal. This makes
it easy to see what the effect of the parameter change is.

If you click on a data point it's label will be shown.

Rankingplot
===========
Bioplot.py allows you to plot a ranking plot. Example run:
python ./bioplot.py -e "ranking plot" -f testdata_A.txt -R

E.g. if looking for a picture in a database a face recognition
system may return a list of potential hits. This plot shows what the
odds are that the target will be in the first N pictures.

Accuracyplot
============
This plot shows the following accuracies for a range of decision thresholds:

                          number of true positives + number of true negatives
random accuracy= -----------------------------------------------------------------------------
                 number of true positives + false positives + false negatives + true negatives


                    sensitivity + specificity
balanced accuracy = -------------------------- =
                                2

                         0.5 * true positives                   0.5 * true negatives
                   --------------------------------  +  ----------------------------------
                   true positives + false negatives      true negatives + false positives

python ./bioplot.py -e "accuracy plot" -f testdata_A.txt -A

Histogram
=========
Need I explain?

Known Issues
============
In data.py the following character sequences are used to group data: '_#_' and '@'.
If they are in your data set, either change your data set or change the characters
in format.py and choose non ambiguous replacements.

Finally:

If you have any questions or feature requests (no guarantees!) or find any bugs,
you can contact me at josbouten@gmail.comMs Windows
==========
Follow the instructions found here: http://matplotlib.org/users/installing.html
I've tried anaconda 2.01 (32 bit version) on W7
This will install python 2.7,7 and a load of python modules amongst which numpy, matplotlib, pyplot
You will be able to run bioplot.py and do much more pythony things ;-)

Copy plot.cf4_4_windows.txt to bioplot.cfg in the working directory (the directory where
bioplot.py is stored) and run the main program ./bioplot.py -h to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them. Their values are shown on the
commandline whenever you run the program, unless you choose not to via the appropriate
option in bioplot.cfg

Linux
=====
You need to have python2.7.x installed. On most linux systems
this is the case.

Then install matplotlib and some other modules:

sudo apt-get install python-matplotlib python-numpy python-scipy

If you get into trouble, talk to your local linux guru. Do not mail me!
Next, copy plot.cf4_4_linux to bioplot.cfg
then run the main program: ./bioplot.py -h to find out how to use it.
Also look at bioplot.cfg to find out about additional options not available
via the command line interface. There are lots of them.

OSX
===
Haven't tried this yet.
So basically you are on your own.
Do mail me a description if you find out how to get things running on
OSX so that I can include it here.


Data file
=========
See manual.txt
